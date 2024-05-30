import django_filters
from django_filters import rest_framework as filters
from .models import Product

class ProductFilter(filters.FilterSet):
    subcategory_name = filters.CharFilter(field_name='subcategory__name', lookup_expr='icontains')
    subcategory_id = django_filters.RangeFilter(field_name='subcategory__id')
    subcategory_serial_number = filters.RangeFilter(field_name='serial_number')
    category_name = filters.CharFilter(field_name='subcategory__category__category_name', lookup_expr='icontains')
    category_id = django_filters.RangeFilter(field_name='subcategory__category__id')
    created_at = filters.DateFilter(field_name='created_at', lookup_expr='exact')
    modified_at = filters.DateFilter(field_name='modified_at', lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['name', 'created_at', 'modified_at', 'subcategory_id', 'subcategory_serial_number', 'category_id']
