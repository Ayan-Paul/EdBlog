from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .decorators import institute_admin_required
from .models import Account, InstituteAdminAccount, StudentAccount, TeacherAccount, UserAccount
from Institute.forms import InstituteForm
from .forms import (InstituteAdminAccountCreationForm, InstituteAdminAccountChangeForm, 
                    StudentAccountCreationForm, StudentAccountChangeForm, StudentAccountEditForm, 
                    TeacherAccountCreationForm, TeacherAccountChangeForm,)
from Post.models import Post, Review


def institute_admin_signup(request, *args, **kwargs):
    form = InstituteAdminAccountCreationForm()
    institute_form = InstituteForm()
    user = request.user
    if user.is_authenticated: 
        return HttpResponse("You are already authenticated as " + str(user.email))
        
    if request.POST:
        form = InstituteAdminAccountCreationForm(request.POST)
        institute_form = InstituteForm(request.POST)
        if form.is_valid() and institute_form.is_valid():
            institute_user = institute_form.save()
            user = form.save(commit=False)
            # user.email = user.email.lower()
            user.username = user.username.lower()
            user.institute = institute_user
            user.save()
            account = authenticate(email=user.email, password=user.password)
            login(request, user)
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect('student-registration', slug=user.institute.slug)
        
    context = {
        'form': form,
        'institute_form': institute_form,
    }
    
    return render(request, 'Account/signup.html', context)

def sign_in(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
   
        try:
            user = UserAccount.objects.get(email=email)
        except:
            messages.error(request, 'Email does not exist')
            return render(request, 'Account/signin.html')

        user = authenticate(request, email=email, password=password)
        
        print(user)
        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'home')
        else:
            messages.error(request, 'Email or password is incorrect')

    return render(request, 'Account/signin.html')

def admin_sign_in(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = InstituteAdminAccount.objects.get(email=email)
        except:
            messages.error(request, 'Email does not exist')
            return render(request, 'Account/admin_signin.html')
    
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('student-registration', slug=user.institute.slug)
        else:
            messages.error(request, 'Email or password is incorrect')

    return render(request, 'Account/admin_signin.html')


def sign_out(request):
    logout(request)
    messages.info(request, 'User logged out')
    return redirect('signin')

@login_required(login_url='admin_signin')
@institute_admin_required
def student_registration(request, slug):
    page = 'sudent_registration'
    form = StudentAccountCreationForm()
    print(request.user.institute)
    if request.POST:
        form = StudentAccountCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.username = user.username.lower()
            user.institute = request.user.institute
            print(user.institute)
            user.save()
            messages.success(request, "Student Account Successfully created!")

            return redirect('student-registration', slug=user.institute.slug)
        
    context = {
        'form': form,
        'page': page,
    }
    
    return render(request, 'Account/user_registration.html', context)

@login_required(login_url='admin_signin')
@institute_admin_required
def teacher_registration(request, slug):
    page = 'teacher_registration'
    UserAccount.default_type = UserAccount.Types.TEACHER
    form = TeacherAccountCreationForm()

    if request.POST:
        form = TeacherAccountCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.username = user.username.lower()
            user.institute = request.user.institute
            user.save()
            messages.success(request, "Teacher Account Successfully created!")

            return redirect('teacher-registration', slug=user.institute.slug)
        
    context = {
        'form': form,
        'page': page,
    }
    
    return render(request, 'Account/user_registration.html', context)

@login_required(login_url='admin_signin')
@institute_admin_required
def view_registered_users(request, slug):
    students = StudentAccount.objects.filter(institute=request.user.institute)
    teachers = TeacherAccount.objects.filter(institute=request.user.institute)

    context = {
        'students': students,
        'teachers': teachers,
    }

    return render(request, 'Account/view_registered_users.html', context)

@login_required(login_url='signin')
def user_profile(reqeust, pk):
    page = 'user_profile'
    user = UserAccount.objects.get(id=pk)

    if user is None:
        return redirect('home')
    
    context = {
        'user_profile': user,
        'page': page,
    }

    return render(reqeust, 'Account/user_profile.html', context)

@login_required(login_url='signin')
def my_user_profile(reqeust):
    page = 'my_user_profile'
    user = UserAccount.objects.get(id=reqeust.user.id)

    if user is None:
        return redirect('signin')

    context = {
        'user_profile': user,
        'page': page,
    }

    return render(reqeust, 'Account/user_profile.html', context)

@login_required(login_url='signin')
def edit_user_profile(request):
    user = UserAccount.objects.get(id=request.user.id)
    form = StudentAccountEditForm(instance=user)

    if request.method == 'POST':
        form = StudentAccountEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

            return redirect('my-user-profile')

    context = {
        'form': form
    }

    return render(request, 'Account/user_profile_edit.html', context)

@institute_admin_required
@login_required(login_url='signin')
def view_posts(request, slug):
    user = request.user
    students_blogs = Post.objects.filter(Q(owner__institute=user.institute) & Q(owner__type='Student'))
    teachers_blogs = Post.objects.filter(Q(owner__institute=user.institute) & Q(owner__type='Teacher'))

    context = {
        'students_blogs': students_blogs,
        'teachers_blogs': teachers_blogs,
    }

    return render(request, 'Account/view_posts.html', context)

@institute_admin_required
@login_required(login_url='admin_signin')
def view_comments(request, slug):
    user = request.user
    students_comments = Review.objects.filter(Q(owner__institute=user.institute) & Q(owner__type='Student'))
    teachers_comments = Review.objects.filter(Q(owner__institute=user.institute) & Q(owner__type='Teacher'))

    context = {
        'students_comments': students_comments,
        'teachers_comments': teachers_comments,
    }

    return render(request, 'Account/view_comments.html', context)

@institute_admin_required
@login_required(login_url='admin_signin')
def edit_user_profile_admin(request, pk, slug):
    user = UserAccount.objects.get(id=pk)
    form = StudentAccountChangeForm(instance=user)

    if request.method == 'POST':
        form = StudentAccountChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

            return redirect('view-registered-users', slug=user.institute.slug)

    context = {
        'form': form
    }

    return render(request, 'Account/user_profile_edit_admin.html', context)


