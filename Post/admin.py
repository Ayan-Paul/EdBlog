from django.contrib import admin
from .models import Post, Category, Review, Tag

class AdminPost(admin.ModelAdmin):
    list_filter = ['publishing_date']
    list_display = ['title', 'vote_ratio', 'publishing_date']
    search_fields = ['title', 'content']

    class Meta:
        model = Post
        
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Tag)