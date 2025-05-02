from django.contrib import admin
from .models import Candidate, Vote, Comment, UserProfile

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'total_votes')
    search_fields = ('name', 'department')
    list_filter = ('department',)

class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'candidate', 'voted_at')
    list_filter = ('candidate', 'voted_at')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'user__username')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_verified', 'voted')
    list_filter = ('is_verified', 'voted')
    search_fields = ('user__username',)

admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
