from django.db import models
from django.template.defaultfilters import slugify
import uuid
from ckeditor.fields import RichTextField
from Account.models import UserAccount
from django.db.models import Q

class Post(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(editable=False)
    content = RichTextField(blank=True, null=True)
    post_image = models.ImageField(max_length=255, upload_to='post_images', null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=1, related_name='posts')
    updated = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(auto_now_add=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    featured = models.BooleanField(default=False)

    class Status(models.TextChoices):
        Accepted = "Accepted", "ACCEPTED"
        Rejected = "Rejected", "REJECTED"
        Pending = "Pending", "PENDING"

    default_status = Status.Pending
    status = models.CharField(max_length=30, choices=Status.choices, default=default_status)

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']

    def __str__(self):
        return self.title

    def post_tag(self):
        return ','.join(str(tag) for tag in self.tag.all())
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    @property
    def comments(self):
        queryset = self.reviews.filter(Q(published=True) & Q(status='Accepted')).count()
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.reviews.all()
        upVotes = reviews.filter(Q(value='up') & Q(published=True) & Q(status='Accepted')).count()
        totalVotes = reviews.count()

        if totalVotes == 0:
            self.vote_total = 0
            self.vote_ratio = 0
            self.save()
            return
        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()

class Category(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(editable=False, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def post_count(self):
        return self.posts.filter(Q(published=True) & Q(status='Accepted')).count()
    
class Review(models.Model) :
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True, related_name="reviews")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name="reviews")
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(auto_now_add=True)

    class Status(models.TextChoices):
        Accepted = "Accepted", "ACCEPTED"
        Rejected = "Rejected", "REJECTED"
        Pending = "Pending", "PENDING"

    default_status = Status.Pending
    status = models.CharField(max_length=30, choices=Status.choices, default=default_status)

    def __str__(self):
        return self.value

class Tag(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def post_count(self):
        return self.posts.all().count()