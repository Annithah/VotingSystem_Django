from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from .models import Candidate, Vote, Comment, UserProfile
from .forms import CustomUserCreationForm, CommentForm
import json

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
            # Ensure UserProfile is created only if it doesn't exist
            UserProfile.objects.get_or_create(user=user)  # Use get_or_create to avoid duplicates
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# User login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, "Invalid username or password")
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
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    comments = Comment.objects.all().order_by('-created_at')
    comment_form = CommentForm()

    return render(request, 'dashboard.html', {
        'candidates': candidates,
        'user_profile': user_profile,
        'comment_form': comment_form,
        'comments': comments
    })

# Submit comment with AJAX
@csrf_exempt
@login_required
def submit_comment(request):
    if request.method == "POST":
        try:
            # Handle both form data and JSON requests
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                text = data.get('text', '').strip()
                is_suggestion = data.get('is_suggestion', False)
            else:
                text = request.POST.get('text', '').strip()
                is_suggestion = request.POST.get('is_suggestion', 'false').lower() == 'true'
            
            if not text:
                return JsonResponse({"error": "Comment cannot be empty"}, status=400)
            
            # Create and save the comment
            comment = Comment.objects.create(
                user=request.user,
                text=text,
                is_suggestion=is_suggestion  # Explicitly set the field
            )
            
            return JsonResponse({
                "success": True,
                "message": "Comment submitted successfully!",
                "comment": {
                    "username": request.user.username,
                    "text": comment.text,
                    "is_suggestion": comment.is_suggestion,
                    "created_at": comment.created_at.strftime("%b %d, %Y %H:%M")
                }
            })
            
        except Exception as e:
            return JsonResponse({
                "error": str(e),
                "details": "An error occurred while processing your comment"
            }, status=500)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

# Vote for a candidate
@login_required
def vote(request, candidate_id):
    try:
        candidate = get_object_or_404(Candidate, pk=candidate_id)
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)

        if user_profile.voted:
            messages.error(request, "You've already voted!")
            return redirect('dashboard')

        Vote.objects.create(user=request.user, candidate=candidate)
        user_profile.voted = True
        user_profile.save()

        messages.success(request, f"Thank you for voting for {candidate.name}!")
        return redirect('dashboard')
        
    except IntegrityError:
        messages.error(request, "You have already voted for this candidate!")
        return redirect('dashboard')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('dashboard')