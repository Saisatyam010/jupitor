from rest_framework import viewsets
import django_filters
from .models import SubCategory
from .serializers import SubCategorySerializer
from .filters import SubCategoryFilter
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from categories.models import Category
from .bulk_operations import bulk_copy_subcategories, bulk_delete_subcategories
class SubCategoryPagination(PageNumberPagination):
    page_size = 30  # Default page size
    page_size_query_param = 'page_size'  # Parameter to dynamically set page size
    max_page_size = 100  # Maximum page size limit

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all().order_by('serial_number')
    serializer_class = SubCategorySerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter]
    filterset_class = SubCategoryFilter
    search_fields = ['id', 'serial_number', 'name']
    pagination_class = SubCategoryPagination

    @action(detail=True, methods=['post'], url_path='copy-to-categories')
    def copy_to_categories(self, request, pk=None):
        try:
            subcategory = self.get_object()
            target_category_ids = request.data.get('category_ids', [])

            if not target_category_ids:
                return Response({'error': 'Category IDs are required'}, status=status.HTTP_400_BAD_REQUEST)

            copied_subcategories = []
            for category_id in target_category_ids:
                try:
                    target_category = Category.objects.get(id=category_id)
                except Category.DoesNotExist:
                    continue  # Skip invalid category IDs

                new_subcategory = SubCategory.objects.create(
                    name=subcategory.name,
                    category=target_category,
                    serial_number=None,  # Serial number will be auto-generated
                )
                new_subcategory.save()
                copied_subcategories.append(new_subcategory.id)

                # Optionally, update subcategory count in the target category
                target_category.subcategory_count = target_category.subcategories.count()
                target_category.save()

            if not copied_subcategories:
                return Response({'error': 'No valid categories found'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'status': 'Subcategory copied to target categories', 'copied_subcategories': copied_subcategories}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='bulk-copy-to-categories')
    def bulk_copy_to_categories(self, request):
        subcategory_ids = request.data.get('subcategory_ids', [])
        target_category_ids = request.data.get('category_ids', [])

        if not subcategory_ids or not target_category_ids:
            return Response({'error': 'Subcategory IDs and Category IDs are required'}, status=status.HTTP_400_BAD_REQUEST)

        copied_subcategories = []
        for subcategory_id in subcategory_ids:
            try:
                subcategory = SubCategory.objects.get(id=subcategory_id)
            except SubCategory.DoesNotExist:
                continue  # Skip invalid subcategory IDs

            for category_id in target_category_ids:
                try:
                    target_category = Category.objects.get(id=category_id)
                except Category.DoesNotExist:
                    continue  # Skip invalid category IDs

                new_subcategory = SubCategory.objects.create(
                    name=subcategory.name,
                    category=target_category,
                    serial_number=None,  # Serial number will be auto-generated
                )
                new_subcategory.save()
                copied_subcategories.append(new_subcategory.id)

                # Optionally, update subcategory count in the target category
                target_category.subcategory_count = target_category.subcategories.count()
                target_category.save()

        if not copied_subcategories:
            return Response({'error': 'No valid subcategories or categories found'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'Subcategories copied to target categories', 'copied_subcategories': copied_subcategories}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='bulk-delete')
    def bulk_delete(self, request):
        django_request = request._request  # Get the underlying HttpRequest
        return bulk_delete_subcategories(django_request)
