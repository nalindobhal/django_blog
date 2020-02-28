from django.urls.conf import path
from django.contrib.auth.views import LogoutView

from .views import (
index, BlogApiView, BlogGetUpdateView,
CustomLoginView, registration_view, LoginView
)

urlpatterns = [
    path('', index, name='index_page'),
    path('blogs/', BlogApiView.as_view(), name='blogs_page'),
    path('blogs/add/', index, name='add_blog'),
    # path(r'^blogs/upload/$', blog_upload_image, name='upload_blog_image'),
    # path(r'^blogs/tags/$', get_tags, name='get_tags'),


    path('blogs/<slug:slug>/', BlogGetUpdateView.as_view(), name='blog_view'),
    # path(r'^category/(?P<slug>[\w.@+-]+)/$', category_view, name='category'),

    # path(r'^api/comment/$', login_required(submit_comment, login_url=settings.REDIRECT_TO_LOGIN), name='comment'),

    # Auth urls
    path('accounts/login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/signup/', registration_view, name='signup'),
    path('accounts/logout/', LogoutView.as_view(next_page="/accounts/login/"), name='logout'),
]