from rest_framework import viewsets, filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Product, SubCategory
from .serializers import ProductSerializer
from .filters import ProductFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .bulk_operations import bulk_delete_products, bulk_copy_products

class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'subcategory__name', 'subcategory__category__category_name']
    ordering_fields = ['serial_number', 'name', 'created_at', 'modified_at']

    @action(detail=True, methods=['post'], url_path='copy-to-subcategory')
    def copy_to_subcategory(self, request, pk=None):
        try:
            product = self.get_object()
            new_subcategory_id = request.data.get('subcategory_id')
            new_subcategory = SubCategory.objects.get(pk=new_subcategory_id)
            last_product = Product.objects.all().order_by('-serial_number').first()
            next_serial_number = last_product.serial_number + 1 if last_product else 1
            new_product = Product.objects.create(
                serial_number=next_serial_number,
                name=product.name,
                subcategory=new_subcategory,
                title_count=product.title_count,
                created_at=product.created_at,
                modified_at=product.modified_at,
                short_desc=product.short_desc,
                long_desc=product.long_desc,
                tags=product.tags,
                selling_price=product.selling_price,
                mrp_price=product.mrp_price,
                images=product.images,
                no_of_prompts=product.no_of_prompts  # Include the new field
            )
            serializer = self.get_serializer(new_product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except SubCategory.DoesNotExist:
            return Response({'error': 'Subcategory not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='bulk-delete')
    def bulk_delete(self, request):
        return bulk_delete_products(request)

    @action(detail=False, methods=['post'], url_path='bulk-copy-to-subcategory')
    def bulk_copy_to_subcategory(self, request):
        return bulk_copy_products(request)

def update_subcategory_product_serial_numbers(subcategory_id):
    products = Product.objects.filter(subcategory_id=subcategory_id).order_by('created_at')
    for index, product in enumerate(products, start=1):
        product.serial_number = index
        product.save(update_fields=['serial_number'])
