from import_export import resources
from .models import Product

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('serial_number', 'id', 'name', 'subcategory__name', 'subcategory__category__name', 'title_count', 'created_at', 'modified_at')
