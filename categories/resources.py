# categories/resources.py
from import_export import resources
from .models import Category

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'category_name', 'serial_number', 'created_at', 'modified_at')
