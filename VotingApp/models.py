from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Candidate model
class Candidate(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='candidates/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.department})"

    @property
    def total_votes(self):
        return self.vote_set.count()

# Vote model
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'candidate')

    def __str__(self):
        return f"{self.user.username} voted for {self.candidate.name}"

# Comment model
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

# User Profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    voted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# Automatically create user profile when a new user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
