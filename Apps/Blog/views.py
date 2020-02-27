from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls.base import reverse
from django.views.decorators.http import require_http_methods

from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import generics

from .models import Article
from .forms import UserCreationForm, ArticleForm
from .serializers import ArticleSerializer


@require_http_methods(['GET', 'POST'])
def registration_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('index_page'))

    if request.method == 'GET':
        return render(request, 'registration/login.html', {'form': UserCreationForm()})

    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        login(request, user)
        return redirect(reverse('index_page'))
    else:
        return render(request, 'registration/login.html', {
            'form': form,
            'errors': [v for k, v in form.errors.items()]
        })


class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('index_page'))
        return super().dispatch(request, *args, **kwargs)


# Blog Views
@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer,))
def index(request):
    blogs = Article.objects.filter(published=True)
    return Response({'blogs': blogs}, template_name='index.html')


class BlogApiView(generics.ListCreateAPIView):

    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.all()

    def get(self, request, *args, **kwargs):
        blogs = Article.objects.filter(published=True)
        return Response({'blogs': blogs, 'form': ArticleForm()}, template_name='index.html')

