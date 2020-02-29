from django.contrib import admin

from .models import Article, ArticleCategory, Comment


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    pass


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Article, ArticleAdmin)
