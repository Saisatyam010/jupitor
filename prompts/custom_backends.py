from django_filters import rest_framework as filters
from .models import Prompt

class PromptFilterBackend(filters.DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        product_id = request.query_params.get('product_id')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset
