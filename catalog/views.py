from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils import timezone
from haystack.views import SearchView
from .models import Category, Product

class CustomSearchView(SearchView):
    def __name__(self):
        return "CustomSearchView"

    def extra_context(self):
        return {
            'category_list':get_list_or_404(Category)
        }

def search_product(request):

    return CustomSearchView(template='search/search_product.html')(request)

class CategoryListView(ListView):

    model = Category
    template_name = 'catalog/category_list.html'  

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['category_list'] = get_list_or_404(Category)
        if 'cid' in self.kwargs:
			category = get_object_or_404(Category, id=self.kwargs['cid'])
			context['category_data'] = category
			context['product_list'] = Product.objects.filter(category=category.id)
        else:
        	context['product_list'] = get_list_or_404(Product)
    	return context


class ProductDetailView(DetailView):

    model = Product
    template_name = 'catalog/product_detail.html'
    slug_field = 'sku'

    def get_context_data(self, **kwargs):
		context = super(ProductDetailView, self).get_context_data(**kwargs)
		context['category_list'] = get_list_or_404(Category)
		#context['related_product_list'] = Product.objects.filter(category=product.catalog)
		return context