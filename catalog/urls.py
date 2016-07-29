from django.conf.urls import include, url
from . import views
from .views import CategoryListView, ProductDetailView
from .views import SearchView, search_product
urlpatterns = [
    url(r'^$', CategoryListView.as_view(), name='catalog_list'),
    url(r'^catalog/$', CategoryListView.as_view(), name='catalog_list'),
    url(r'^catalog/(?P<cid>\d+)/$', CategoryListView.as_view(), name='view_catalog'),
    url(r'^catalog/product/(?P<slug>\d+)/$', ProductDetailView.as_view(), name='view_product'),
    url(r'^search/', include('haystack.urls')),
    url(r'^search/product/', search_product, name='search_product'),
]
