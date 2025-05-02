from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Candidate, Vote, Comment, UserProfile
from .forms import CustomUserCreationForm, CommentForm

# Home page
def home(request):
    candidates = Candidate.objects.all()[:4]  # Top 4 candidates for homepage
    return render(request, 'home.html', {'candidates': candidates})

# User registration
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# User login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']  # Make sure your form uses 'password1' as the input name
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

# User logout
@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

# Dashboard
@login_required
def dashboard(request):
    candidates = Candidate.objects.all()
    user_profile = request.user.userprofile
    comments = Comment.objects.all().order_by('-created_at')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.save()
            messages.success(request, "Your comment was sent successfully!")
            return redirect('dashboard')
    else:
        comment_form = CommentForm()

    return render(request, 'dashboard.html', {
        'candidates': candidates,
        'user_profile': user_profile,
        'comment_form': comment_form,
        'comments': comments
    })

# Vote for a candidate
@login_required
def vote(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)

    if request.user.userprofile.voted:
        messages.error(request, "You've already voted!")
        return redirect('dashboard')

    Vote.objects.create(user=request.user, candidate=candidate)
    request.user.userprofile.voted = True
    request.user.userprofile.save()

    messages.success(request, f"Hello {request.user.username}, you have voted for {candidate.name} - {candidate.description}")
    return redirect('dashboard')
