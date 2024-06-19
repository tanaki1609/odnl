from rest_framework import serializers
from .models import Product, Category, Tag
from rest_framework.exceptions import ValidationError


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


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=5, max_length=100)
    price = serializers.FloatField(min_value=1, max_value=1000000)
    description = serializers.CharField(required=False)
    is_active = serializers.BooleanField()
    category_id = serializers.IntegerField(min_value=1)
    tags = serializers.ListField(child=serializers.IntegerField(min_value=1))

    # def validate(self, attrs):
    #     category_id = attrs['category_id']
    #     try:
    #         Category.objects.get(id=category_id)
    #     except Category.DoesNotExist:
    #         raise ValidationError('Category not found')
    #     return attrs

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Category not found')
        return category_id

    def validate_tags(self, tags):  # [1,2,100]
        tags_from_db = Tag.objects.filter(id__in=tags)  # [1,2]
        if len(tags_from_db) != len(tags):
            raise ValidationError('Tag not found')
        return tags
