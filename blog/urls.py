from django.conf.urls import include, url
from . import views
from .views import BlogListView, PostDetailView
from .views import SearchView, blog_search
urlpatterns = [
    url(r'^blog/$', BlogListView.as_view(), name='blog_list'),
    url(r'^blog/(?P<cid>\d+)/$', BlogListView.as_view(), name='view_blog'),
    url(r'^post/(?P<pk>\d+)/$', PostDetailView.as_view(), name='view_post'),
    url(r'^blog/search/', blog_search, name='blog_search'),
]
