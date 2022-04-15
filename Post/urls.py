from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teachers-blogs/', views.teachers_blogs, name='teachers-blogs'),
    path('students-blogs/', views.students_blogs, name='students-blogs'),
    path('category/<slug:slug>/', views.category_blogs, name='category'),
    path('tag/<slug:slug>/', views.tag_blogs, name='tag'),
    path('blog/<str:pk>/', views.single_blog, name='single-blog'),
    path('create-blog/', views.create_blog, name='create-blog'),
    path('update-blog/<str:pk>/', views.update_blog, name='update-blog'),
    path('edit-blog-admin/<str:pk>/', views.edit_blog_admin, name='edit-blog-admin'),
    path('edit-comment-admin/<str:pk>/', views.edit_comment_admin, name='edit-comment-admin'),
    
]