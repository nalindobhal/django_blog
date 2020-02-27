from django.urls.conf import path
from django.contrib.auth.views import LogoutView

from .views import (
index, BlogApiView,
CustomLoginView, registration_view, LoginView
)

urlpatterns = [
    path('', index, name='index_page'),
    path('blogs/', BlogApiView.as_view(), name='index_page'),
    path('blogs/add/', BlogApiView.as_view(), name='add_blog'),
    # path(r'^blogs/sanitize/$', sanitize_blog, name='sanitize_blog'),
    # path(r'^blogs/upload/$', blog_upload_image, name='upload_blog_image'),
    # path(r'^blogs/tags/$', get_tags, name='get_tags'),

    # path(r'^blogs/(?P<token>[\w.@+-]+)/edit/$', EditBlog.as_view(), name='blog-edit'),


    # path(r'^blogs/(?P<slug>[\w.@+-]+)/$', blog_view, name='blog'),
    # path(r'^category/(?P<slug>[\w.@+-]+)/$', category_view, name='category'),

    # path(r'^api/comment/$', login_required(submit_comment, login_url=settings.REDIRECT_TO_LOGIN), name='comment'),

    # Auth urls
    path('accounts/login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/signup/', registration_view, name='signup'),
    path('accounts/logout/', LogoutView.as_view(next_page="/accounts/login/"), name='logout'),
]