from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils import timezone
from haystack.views import SearchView
from .models import Category, Post

class CustomSearchView(SearchView):
    def __name__(self):
        return "CustomSearchView"

    def extra_context(self):
        return {
            'category_list':get_list_or_404(Category)
        }

def blog_search(request):

    return CustomSearchView(template='search/search_post.html')(request)

class BlogListView(ListView):

    model = Category
    template_name = 'blog/category_list.html'  

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        if 'cid' in self.kwargs:
			category = get_object_or_404(Category, id=self.kwargs['cid'])
			context['category_data'] = category
			context['post_list'] = Post.objects.filter(category=category.id)
        else:
        	context['post_list'] = get_list_or_404(Post)
    	return context


class PostDetailView(DetailView):

    model = Post
    template_name = 'blog/post_detail.html'  

    def get_context_data(self, **kwargs):
		context = super(PostDetailView, self).get_context_data(**kwargs)
		context['category_list'] = get_list_or_404(Category)
		return context