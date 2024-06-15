from rest_framework import serializers
from .models import Product, Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id name'.split()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = 'name'.split()


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    tag_names = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'reviews id title price category_name tag_names category tags'.split()
        depth = 1
        # exclude = 'id'.split()

    def get_tag_names(self, product):
        return [tag.name for tag in product.tags.all()]
