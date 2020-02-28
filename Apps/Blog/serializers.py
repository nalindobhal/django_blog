from uuid import uuid4

from rest_framework.serializers import ModelSerializer

from .models import Article


class ArticleSerializer(ModelSerializer):

    class Meta:
        model = Article
        exclude = ['slug', 'published_by', 'published_on']
        

    def create(self, validated_data):
    	categories = validated_data.pop('category')
    	slug = "-".join([validated_data['name'], str(uuid4())])
    	article = Article.objects.create(slug=slug, **validated_data)
    	for cat in categories:
    		article.category.add(cat)
    	return article