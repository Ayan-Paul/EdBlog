from django import forms
from .models import Post, Review

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'post_image', 'category', 'tags')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'bg-white'})

class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'post_image', 'category', 'tags', 'published', 'featured', 'status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'bg-white'})
        self.fields['published'].widget.attrs.update({'class': 'ml-5'})
        self.fields['featured'].widget.attrs.update({'class': 'ml-5'})

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('body', 'value')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs.update({'class': 'form-control mb-10'})
        self.fields['value'].widget.attrs.update({'class': 'form-control pb-2'})

class EditReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('body', 'value', 'published', 'status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs.update({'style': 'height: 5rem'})
        self.fields['published'].widget.attrs.update({'class': 'ml-5'})

 