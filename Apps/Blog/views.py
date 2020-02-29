import json

from PIL import Image
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.core.files.storage import FileSystemStorage
from django.db.models.functions import datetime
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls.base import reverse
from django.views.decorators.http import require_http_methods

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import generics

from modules.utils import generate_upload_path
from .models import Article
from .forms import UserCreationForm
from .serializers import ArticleSerializer, ArticleReadSerializer, CommentWriteSerializer
from .permissions import IsOwner


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
    return Response(template_name='index.html')


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((TemplateHTMLRenderer,))
def blog_add(request):
    serializer = ArticleSerializer()
    return Response(
        {
            'serializer': serializer,
            'data': json.dumps(serializer.data),
            'source': 'Add',
            'form_url': reverse('blogs_page')
        },
        template_name='blogs/add_blog.html')


class BlogApiView(generics.ListCreateAPIView):
    serializer_class = ArticleSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'blogs/blogs.html'

    def get_queryset(self):
        return Article.objects.all()

    def get(self, request, *args, **kwargs):
        blogs = Article.objects.all()
        return Response({'blogs': blogs, 'form_url': reverse('blogs_page')})

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(published_by=self.request.user)
            return redirect(reverse('blog_view', kwargs={'blog_slug': instance.slug}))
        return Response({
            'serializer': serializer,
            'errors': serializer.errors,
            'data': json.dumps(serializer.data),
            'source': 'Add',
            'form_url': reverse('blogs_page')
        }, template_name='blogs/add_blog.html')

    def perform_create(self, serializer):
        serializer.save(published_by=self.request.user)


class BlogGetView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'blogs/blog_page.html'
    lookup_field = 'slug'
    lookup_url_kwarg = 'blog_slug'

    def get_object(self):
        return get_object_or_404(Article, slug=self.kwargs['blog_slug'])

    def get_serializer_class(self):
        return ArticleReadSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        print(serializer.data)
        return Response({'blog': serializer.data})


class BlogUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    renderer_classes = [TemplateHTMLRenderer]
    parser_classes = [MultiPartParser, FormParser]
    template_name = 'blogs/add_blog.html'
    lookup_field = 'slug'
    lookup_url_kwarg = 'blog_slug'
    http_method_names = ['get', "post"]

    def get_object(self):
        obj = get_object_or_404(Article, slug=self.kwargs['blog_slug'])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        form_url = reverse('blog_update', kwargs={'blog_slug': self.kwargs['blog_slug']})
        serializer = ArticleSerializer(instance=self.get_object())
        return Response(
            {
                'serializer': serializer,
                'data': json.dumps(serializer.data),
                'form_url': form_url,
                'source': 'Update',
                'blog_slug': self.kwargs['blog_slug']
            }
        )

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        data = super().update(request, *args, **kwargs)
        return redirect(reverse('blog_view', kwargs={'blog_slug': self.kwargs['blog_slug']}))


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def submit_comment(request, blog_slug):
    article = get_object_or_404(Article, slug=blog_slug)
    comment = CommentWriteSerializer(data=request.data)
    if comment.is_valid(raise_exception=True):
        comment.save(**{'comment_by': request.user, 'article': article})
    return redirect(reverse('blog_view', kwargs={'blog_slug': blog_slug}))


# @require_http_methods(['POST'])
# def blog_upload_image(request):
#     blog_token = request.POST.get("blog_slug")
#     if blog_token is None:
#         context = {"status": "error", "msg": "Blog Does not exist", "token": blog_token}
#         return JsonResponse(context)
#
#     try:
#         blog_instance = Article.objects.get(slug=blog_token)
#     except Article.DoesNotExist as e:
#         print("blog upload image, Article DND ", e)
#         context = {"status": "error", "msg": "Blog does not exist", "token": blog_token}
#         return JsonResponse(context)
#
#     if request.user.id != blog_instance.published_by_id:
#         context = {"status": "error", "msg": "Unauthorised", "token": blog_token}
#         return JsonResponse(context, status=403)
#
#     if len(request.FILES) == 1:
#         request.files = request.FILES
#
#     filename = request.FILES["image"].name
#
#     pil_img = Image.open(request.FILES.get('image'))
#     media_article_path = generate_upload_path(blog_instance, filename)
#     fs = FileSystemStorage(location=media_article_path)
#     filename = fs.save(filename, request.FILES['image'])
#     save_path = media_article_path + filename
#     pil_img.save(save_path, pil_img.format, quality=60)
#
#     context = {
#         "status": "ok",
#         "url": "%s://%s/%s" % (
#             request.scheme, request.get_host(), 'media/' + media_article_path
#         ),
#     }
#     return JsonResponse(context)
