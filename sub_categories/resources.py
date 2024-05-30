# sub_categories/resources.py
from import_export import resources
from .models import SubCategory

class SubCategoryResource(resources.ModelResource):
    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'category', 'serial_number', 'product_count', 'created_at', 'modified_at')
