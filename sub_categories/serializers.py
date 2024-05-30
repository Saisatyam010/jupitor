from rest_framework import serializers
from .models import SubCategory

class SubCategorySerializer(serializers.ModelSerializer):
    s_no = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    modified_at = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()  # Add this line

    class Meta:
        model = SubCategory
        fields = ['s_no', 'id', 'name', 'category', 'category_name', 'created_at', 'modified_at', 'product_count']
        read_only_fields = ['id', 's_no', 'created_at', 'modified_at', 'product_count']

    def get_s_no(self, obj):
        return obj.serial_number

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")

    def get_modified_at(self, obj):
        return obj.modified_at.strftime("%d-%m-%Y %H:%M:%S")

    def get_category_name(self, obj):
        return obj.category.category_name if obj.category else None  # Fetch the category name
