from uuid import uuid4

from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.timesince import timesince
from rest_framework import serializers

from .models import Article, ArticleCategory, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = ['name']


class CommentReadSerializer(serializers.ModelSerializer):
    comment_by = serializers.SerializerMethodField()
    initials = serializers.SerializerMethodField()
    created_on = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_initials(self, obj):
        if obj.comment_by.first_name and obj.comment_by.last_name:
            initials = (f"{obj.comment_by.first_name}"[0] + f"{obj.comment_by.last_name}"[0])
        else:
            initials = f"{obj.comment_by.username}"[0:2]
        return initials.upper()

    def get_comment_by(self, obj):
        return {
            'id': obj.comment_by.id,
            'full_name': f"{obj.comment_by.get_full_name()}",
            'username': obj.comment_by.username
        }

    def get_created_on(self, obj):
        return f"{timesince(obj.created_on)}"


class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['comment_by', 'article']


class ArticleReadSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format='%d-%b-%Y', required=False)
    categories = serializers.SerializerMethodField()
    published_by = serializers.SerializerMethodField()
    comments = CommentReadSerializer(source='comment', many=True)

    def get_categories(self, obj):
        return [i.name for i in obj.category.all()]

    def get_published_by(self, obj):
        return {'id': obj.published_by.id, 'full_name': f"{obj.published_by.get_full_name()}"}

    class Meta:
        model = Article
        fields = ['id', 'name', 'slug', 'intro', 'blog', 'wallpaper', 'categories', 'category', 'created_on',
                  'published_by', 'comments']


class ArticleSerializer(serializers.ModelSerializer):
    blog = serializers.CharField(style={'base_template': 'blog_field.html'}, required=True)
    intro = serializers.CharField(required=True)
    name = serializers.CharField(required=True)

    class Meta:
        model = Article
        exclude = ['slug', 'published_by']

    def create(self, validated_data):
        categories = validated_data.pop('category')
        slug = "-".join([slugify(validated_data['name']), str(uuid4())])
        article = Article.objects.create(slug=slug, **validated_data)
        for cat in categories:
            article.category.add(cat)
        return article

    def update(self, instance, validated_data):
        if validated_data['wallpaper'] is None:
            validated_data['wallpaper'] = instance.wallpaper
        instance = super().update(instance, validated_data)
        return instance
