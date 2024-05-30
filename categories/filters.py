import django_filters
from .models import Category
from datetime import datetime

class CustomDateFilter(django_filters.Filter):
    def filter(self, qs, value):
        if value:
            try:
                value = datetime.strptime(value, '%d-%m-%Y').strftime('%Y-%m-%d')
                lookup_expr = f"{self.field_name}__{self.lookup_expr}"
                qs = qs.filter(**{lookup_expr: value})
            except ValueError:
                raise django_filters.exceptions.ValidationError('Enter a valid date in the format DD-MM-YYYY.')
        return qs

class CategoryFilter(django_filters.FilterSet):
    serial_number = django_filters.RangeFilter()
    id = django_filters.RangeFilter()
    created_at_after = CustomDateFilter(field_name='created_at', lookup_expr='gte')
    created_at_before = CustomDateFilter(field_name='created_at', lookup_expr='lte')
    modified_at_after = CustomDateFilter(field_name='modified_at', lookup_expr='gte')
    modified_at_before = CustomDateFilter(field_name='modified_at', lookup_expr='lte')

    class Meta:
        model = Category
        fields = ['serial_number', 'id', 'created_at_after', 'created_at_before', 'modified_at_after', 'modified_at_before']
