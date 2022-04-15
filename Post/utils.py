from .models import Post, Tag, Category
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginatePosts(request, posts, results):
    page = request.GET.get('page')
    paginator = Paginator(posts, results)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        posts = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        posts = paginator.page(page)


    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, posts

def searchPosts(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(title__icontains=search_query)

    posts = Post.objects.distinct().filter(published=True).filter(status='Accepted').filter(
        Q(title__icontains=search_query) | 
        Q(category__title__icontains=search_query) | 
        Q(owner__first_name__icontains=search_query) |
        Q(owner__last_name__icontains=search_query) |
        Q(owner__institute__name__icontains=search_query) |
        Q(tags__in=tags)
        )
    return posts, search_query