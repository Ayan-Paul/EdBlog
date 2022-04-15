from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Account.models import UserAccount
from .models import Post, Category, Tag, Review
from django.db.models import Q
from .forms import PostForm, EditPostForm, ReviewForm, EditReviewForm
from .utils import paginatePosts, searchPosts
from Account.decorators import institute_admin_required

def home(request):
    posts, search_query = searchPosts(request)
    # posts = Post.objects.filter(published=True)

    custom_ranges, posts = paginatePosts(request, posts, 5)

    context = {
        'blogs': posts,
        'custom_ranges': custom_ranges,
        'search_query': search_query,
    }

    return render(request, 'Post/home.html', context)

def teachers_blogs(request):
    blogs = Post.objects.filter(Q(published=True) & Q(status='Accepted') & Q(owner__type='Teacher'))

    context = {
        'blogs': blogs,
    }

    return render(request, 'Post/home.html', context)

def students_blogs(request):
    blogs = Post.objects.filter(Q(published=True) & Q(status='Accepted') & Q(owner__type='Student'))

    context = {
        'blogs': blogs,
    }

    return render(request, 'Post/home.html', context)

def category_blogs(request, slug):
    blogs = Post.objects.filter(Q(published=True) & Q(status='Accepted') & Q(category__slug=slug))
    category = Category.objects.get(slug=slug)
    context = {
        'blogs': blogs,
        'category': category,
    }

    return render(request, 'Post/home.html', context)

def tag_blogs(request, slug):
    blogs = Post.objects.filter(Q(published=True) & Q(status='Accepted') & Q(tags__slug=slug))
    tag = Tag.objects.get(slug=slug)
    context = {
        'blogs': blogs,
        'tag': tag,
    }

    return render(request, 'Post/home.html', context)

def single_blog(request, pk):
    blog = Post.objects.get(id=pk)
    
    comments = Review.objects.filter(Q(published=True) & Q(status='Accepted') & Q(post__id=blog.id))
    form = ReviewForm()

    if request.method == 'POST':
        if request.user.is_authenticated:
            user_id = request.user.id
            user = UserAccount.objects.get(id=user_id)

        else:
            return redirect('signin')
        
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = blog
            comment.owner = user
            comment.save()
            messages.success(request, 'Comment Successful')
            return redirect('single-blog', pk=blog.id)

    blog.getVoteCount

    context = {
        'form': form,
        'blog': blog,
        'comments': comments,
    }

    return render(request, 'Post/single_blog.html', context)

@login_required(login_url='signin')
def create_blog(request):
    user_id = request.user.id
    user = UserAccount.objects.get(id=user_id)
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.owner = user
            blog.save()

            return redirect('home')

    context = {
        'form': form,
    }

    return render(request, 'Post/create_blog.html', context)

@login_required(login_url='signin')
def update_blog(request, pk):
    blog = Post.objects.get(id=pk)
    form = PostForm(instance=blog)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()

            return redirect('single-blog', pk=pk)

    context = {
        'form': form,
    }

    return render(request, 'Post/update_blog.html', context)

@login_required(login_url='admin_signin')
@institute_admin_required
def edit_blog_admin(request, pk):
    blog = Post.objects.get(id=pk)
    form = EditPostForm(instance=blog)

    if request.method == 'POST':
        form = EditPostForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()

            return redirect('view-posts', slug=request.user.institute.slug)

    context = {
        'form': form,
    }

    return render(request, 'Post/edit_blog_admin.html', context)

@login_required(login_url='admin_signin')
@institute_admin_required
def edit_comment_admin(request, pk):
    comment = Review.objects.get(id=pk)
    form = EditReviewForm(instance=comment)

    if request.method == 'POST':
        form = EditReviewForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()

            return redirect('view-comments', slug=request.user.institute.slug)

    context = {
        'form': form,
    }

    return render(request, 'Post/edit_comment_admin.html', context)
