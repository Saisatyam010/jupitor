from rest_framework import serializers
from .models import Prompt

class PromptSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    subcategory_name = serializers.CharField(source='product.subcategory.name', read_only=True)
    category_name = serializers.CharField(source='product.subcategory.category.category_name', read_only=True)

    class Meta:
        model = Prompt
        fields = [
            'id',
            'serial_number',
            'product',
            'product_name',
            'subcategory_name',
            'category_name',
            'created_at',
            'modified_at',
            'no_of_titles',
            'prompt_text',
            'times_generated'  # Include the new field
        ]
