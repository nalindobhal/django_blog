from django.contrib.auth.decorators import login_required
from django.urls.conf import path
from django.contrib.auth.views import LogoutView

from .views import (
    index, blog_add, BlogApiView, BlogGetView, BlogUpdateView, submit_comment,
    CustomLoginView, registration_view, LoginView
)

urlpatterns = [
    path('', index, name='index_page'),
    path('blogs/', BlogApiView.as_view(), name='blogs_page'),
    path('blogs/add/', blog_add, name='add_blog'),
    # path('blogs/upload/', login_required(blog_upload_image), name='upload_blog_image'),

    # dynamic url should be at last
    path('blogs/<slug:blog_slug>/', BlogGetView.as_view(), name='blog_view'),
    path('blogs/<slug:blog_slug>/edit', BlogUpdateView.as_view(), name='blog_update'),
    path('blogs/<slug:blog_slug>/comment/', login_required(submit_comment),
         name='comment_add'),

    # Auth urls
    path('accounts/login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/signup/', registration_view, name='signup'),
    path('accounts/logout/', LogoutView.as_view(next_page="/"), name='logout'),
]
