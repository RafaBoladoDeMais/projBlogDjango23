from typing import Any, Dict
from django import http
from django.core.paginator import Paginator
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from blog.models import Post, Page, Category
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404, HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView


posts = list(range(1000))
# Create your views here.
PER_PAGE = 9

class PostListView(ListView):
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()
    # def get_queryset(self):
    #     queryset = super().get_queryset().filter(is_published=True)

    #     return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'home - ',
        })
        return context

class CreatedByListView(PostListView):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs) 
        self._temp_ctx: dict[str, Any] = {}

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        author_id = self.kwargs.get('auth_id')
        user = User.objects.filter(id=author_id).first()

        if user is None:
            raise Http404()
        
        self._temp_ctx.update({
            'user': user,
            'author_id': author_id,
        })
        
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset().filter(created_by=self.kwargs.get('auth_id'))

        return qs 

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
         
        user = self._temp_ctx['user']
        
        user_full_name = user.username

        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'

        page_title = f'Posts de {user_full_name} - '

        ctx.update({'page_title': page_title})
        return ctx


class CategoryListView(PostListView):
    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset().filter(category__slug=self.kwargs.get('slug'))
        return qs
     
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        print(self.kwargs)
        category = Category.objects.filter(slug=self.kwargs.get('slug')).first()

        page_title = f'Catefory - {category} - '
        ctx.update({
            'page_title': page_title,
        })
        
        return ctx

class TagListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset().filter(tags__slug=self.kwargs.get('slug'))
        return qs   
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = f"Tag - {self.object_list[0].tags.filter(slug=self.kwargs.get('slug')).first()} - " #type: ignore

        ctx.update({
            'page_title': page_title,
        })
        return ctx 
    
class SearchListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._search_value = ''

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self._search_value = request.GET.get('search').strip()#type: ignore

        return super().setup(request, *args, **kwargs)
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not self._search_value:
            return redirect('blog:index')
        
        return super().get(request, *args, **kwargs)
    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset().filter(
        Q(title__icontains=self._search_value) |
        Q(excerpt__icontains=self._search_value) |
        Q(content__icontains=self._search_value)
    )[:PER_PAGE]
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        search_v = f'Search - {self._search_value} - '
                
        ctx.update({
            'page_title': search_v,
            'search_value': self._search_value,
        })

        return ctx

class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/pages/page.html'
    # slug_field = 'slug'
    # context_object_name = 'page'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        page_title = ctx['page']
        ctx.update({
            'page_title': f'{page_title} - ',
        })
        return ctx
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/pages/post.html'
    # slug_field = 'slug'
    # context_object_name = 'page'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        page_title = ctx['post']

        ctx.update({
            'page_title': f'{page_title} - ',
        })
        return ctx
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)
    
