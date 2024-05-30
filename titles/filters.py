import django_filters
from .models import Title

class TitleFilter(django_filters.FilterSet):
    created_at_range = django_filters.DateTimeFromToRangeFilter(field_name="created_at")
    modified_at_range = django_filters.DateTimeFromToRangeFilter(field_name="modified_at")
    id_range = django_filters.NumericRangeFilter(field_name="id")
    serial_number_range = django_filters.NumericRangeFilter(field_name="serial_number")

    class Meta:
        model = Title
        fields = ['id_range', 'serial_number_range', 'created_at_range', 'modified_at_range', 'product', 'prompt']
