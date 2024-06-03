from django.shortcuts import render,get_object_or_404, redirect
from .models import Post,Category,Comment,Like
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})

def home(request):
    query = request.GET.get('q', '')
    selected_category = request.GET.get('category', '')

    if selected_category:
        posts = Post.objects.filter(category_id=selected_category)
    else:
        posts = Post.objects.all()

    if query:
        posts = posts.filter(title__icontains=query)

    # Pagination
    paginator = Paginator(posts, 10)  # Show 8 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'query': query,
    }
    
    return render(request, 'home.html', context)

@login_required  
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment_text = request.POST.get('comment')
    if comment_text:
        comment = Comment(post=post, text=comment_text, author=request.user)
        comment.save()
    else:
        # Handle empty comment error
        messages.error(request, 'Please enter a comment.') 
        return redirect('post_detail', post_id=post.id)
    
    # Redirect back to post detail page after adding comment
    return redirect('post_detail', post_id=post.id)

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'You have successfully registered.')  # Add success message
            return redirect('register')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')  # Add error message
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to your home page after successful login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')    

def custom_logout(request):
    logout(request)
    return redirect('login')  


def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    
    # Check if the user has already liked the post
    if Like.objects.filter(post=post, user=user).exists():
        # User has already liked the post, delete the existing like (unlike)
        Like.objects.filter(post=post, user=user).delete()
    else:
        # User has not liked the post before, create a new Like object (like)
        like = Like.objects.create(post=post, user=user)
        # You can perform any additional actions here, such as updating the post's like count

    # Redirect back to the post detail page
    return redirect('post_detail', post_id=post.id) 