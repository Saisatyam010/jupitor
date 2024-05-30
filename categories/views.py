from rest_framework import viewsets
import django_filters
from .models import Category
from .serializers import CategorySerializer
from .filters import CategoryFilter
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from .bulk_operations import bulk_delete_categories

class CategoryPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'  # Parameter to dynamically set page size
    max_page_size = 100  # Maximum page size limit

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('serial_number')
    serializer_class = CategorySerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter]
    filterset_class = CategoryFilter
    search_fields = ['category_name']
    pagination_class = CategoryPagination

    @action(detail=False, methods=['post'])
    def bulk_delete(self, request):
        return bulk_delete_categories(request)
