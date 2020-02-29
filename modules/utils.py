import datetime

from django.template.defaultfilters import truncatewords
from django.utils.text import slugify


def create_slug(content, post_fix=None):
    if post_fix:
        return slugify(content) + "-" + post_fix
    return slugify(content)


def generate_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/Article/article_<id>/<filename>
    model_name = ''
    if len(filename) > 100:
        filename = datetime.datetime.now().__str__()
    try:
        model_name = str(instance._meta.db_table).lower()
    except Exception as e:
        print(e)
        model_name = 'EE'
    return 'Article/article_{0} {1}/{2}/{3}'.format(instance.id, truncatewords(instance.slug, 10), model_name,
                                                              filename)
