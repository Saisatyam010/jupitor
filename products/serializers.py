from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    category_id = serializers.IntegerField(source='subcategory.category.id', read_only=True)
    category_name = serializers.CharField(source='subcategory.category.category_name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'serial_number',
            'name',
            'subcategory',
            'subcategory_name',
            'category_id',
            'category_name',
            'title_count',
            'created_at',
            'modified_at',
            'short_desc',
            'long_desc',
            'tags',
            'selling_price',
            'mrp_price',
            'images',
            'no_of_prompts'  # New field
        ]
        extra_kwargs = {
            'selling_price': {'required': False},
            'mrp_price': {'required': False}
        }
