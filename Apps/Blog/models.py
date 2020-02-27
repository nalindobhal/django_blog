from django.db import models
from django.conf import settings
from django.urls.base import reverse

from modules.utils import generate_upload_path, create_slug


class BaseAppModel(models.Model):
    """This is the base model for other models. This will provide fields for other models. Hence abstract =
    True"""

    name = models.CharField('name', max_length=255, db_index=True, null=True, blank=True,
                            help_text='this field will be used as name for models inheriting from this model')
    created_on = models.DateTimeField('created on', auto_now_add=True, auto_now=False)
    updated_on = models.DateTimeField('updated on', auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return '%s-%s' % (self.id, self.name)


class ArticleCategory(BaseAppModel):

    slug = models.SlugField('slug', max_length=50, blank=True, db_index=True)
    photo = models.ImageField('photo', null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, db_index=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'article_category'
        unique_together = ('name', 'slug',)

    def __str__(self):
        return '%s - %s' % (self.id, self.name)

    @property
    def get_absolute_url(self):
        return reverse('blogs:category', kwargs={'slug': self.slug})

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = create_slug(self.name)
        super().save(force_insert=False, force_update=False, using=None,
                     update_fields=None)


class Article(BaseAppModel):

    category = models.ManyToManyField(ArticleCategory, related_name='category', db_index=True,
                                      help_text="Categories mentioned in the article.")

    slug = models.CharField('slug', max_length=500, db_index=True, unique=True,
                            help_text="slug of an article. It should be unique.")

    blog = models.TextField(null=True, blank=True)
    intro = models.TextField('intro', max_length=500, help_text='Brief of your article in 50-60 words.')

    wallpaper = models.ImageField('wallpaper', max_length=300, null=True, blank=True, upload_to=generate_upload_path,
                                  help_text="wallpaper for the article. This image and its thumbnail "
                                            "will be used everywhere.")

    published_on = models.DateTimeField('published on', null=True, blank=True,
                                        help_text="date when the article was published.")
    published_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user", db_index=True,
                                     help_text="User who published the article.", on_delete=models.CASCADE)

    published = models.BooleanField('published', default=False, db_index=True,
                                    help_text="If an article is published or not. "
                                              "By default an article will be considered as draft.")

    class Meta:
        verbose_name_plural = "Blog"
        verbose_name = "Blogs"
        db_table = "articles"
        ordering = ['-id']

    def __str__(self):
        return '%s-%s' % (self.id, self.name)

    # @property
    # def get_absolute_url(self):
    #     return reverse('blog', kwargs={'slug': self.slug})


# Comments model
class Comment(BaseAppModel):
    STATUS = (
        (1, 'Allowed'),
        (2, 'Deleted'),
        (3, 'Spam'),
    )
    comment = models.TextField('comment')
    # image = models.FileField(null=True, blank=True, upload_to=generate_comment_upload_path,
    #                          help_text="image for the comment")

    article = models.ForeignKey(Article, db_index=True, related_name="comment", on_delete=models.CASCADE)
    comment_by = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True, related_name='comment_by',
                                   on_delete=models.CASCADE)

    status = models.PositiveIntegerField('status', choices=STATUS, default=1)
    is_edited = models.BooleanField('is_edited', default=False)

    class Meta:
        verbose_name_plural = "Comments"
        verbose_name = "Comment"
        db_table = "comment"
        ordering = ['-created_on']

    def __str__(self):
        return '%s' % self.comment[0:30]
