# categories/serializers.py
from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    s_no = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    modified_at = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['s_no', 'id', 'category_name', 'created_at', 'modified_at', 'subcategory_count']
        read_only_fields = ['id', 's_no', 'created_at', 'modified_at', 'subcategory_count']

    def get_s_no(self, obj):
        return obj.serial_number

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")

    def get_modified_at(self, obj):
        return obj.modified_at.strftime("%d-%m-%Y %H:%M:%S")
'}?{'