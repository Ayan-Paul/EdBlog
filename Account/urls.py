from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.institute_admin_signup, name='signup'),
    path('signin/', views.sign_in, name='signin'),
    # admin
    path('admin-signin/', views.admin_sign_in, name='admin_signin'),
    path('signout/', views.sign_out, name='signout'),
    path('<slug:slug>/student-registration', views.student_registration, name='student-registration'),
    path('<slug:slug>/teacher-registration', views.teacher_registration, name='teacher-registration'),
    path('<slug:slug>/view-registered-users', views.view_registered_users, name='view-registered-users'),
    path('<slug:slug>/edit-user-profile-admin/<str:pk>/', views.edit_user_profile_admin, name="edit-user-profile-admin"),
    path('<slug:slug>/view-posts/', views.view_posts, name="view-posts"),
    path('<slug:slug>/view-comments/', views.view_comments, name="view-comments"),

    # User
    path('user-profile/<str:pk>', views.user_profile, name="user-profile"),
    path('my-user-profile/', views.my_user_profile, name="my-user-profile"),
    path('edit-user-profile/', views.edit_user_profile, name="edit-user-profile"),
]