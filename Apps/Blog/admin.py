from django.contrib import admin

from .models import Article, ArticleCategory, Comment


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
