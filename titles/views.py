from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Title
from .serializers import TitleSerializer
from prompts.models import Prompt
from products.models import Product
from .bulk_operations import bulk_delete_titles, bulk_copy_titles_to_products, copy_titles_to_product

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        prompt_id = instance.prompt_id
        self.perform_destroy(instance)
        self.update_related_tables(prompt_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update_related_tables(self, prompt_id):
        prompt = Prompt.objects.get(id=prompt_id)
        prompt.no_of_titles = prompt.prompt_titles.count()  # Use the reverse relationship
        prompt.title_name = "; ".join([title.title_name for title in prompt.prompt_titles.all()])
        prompt.save(update_fields=['no_of_titles', 'title_name'])

        # Update the title count in the product as well
        product = prompt.product
        product.title_count = Title.objects.filter(product=product).count()
        product.save(update_fields=['title_count'])

    @action(detail=False, methods=['post'], url_path='bulk_delete')
    def bulk_delete(self, request):
        return bulk_delete_titles(request)

    @action(detail=False, methods=['post'], url_path='bulk_copy_to_products')
    def bulk_copy_to_products(self, request):
        return bulk_copy_titles_to_products(request)

    @action(detail=True, methods=['post'], url_path='copy_to_product')
    def copy_to_product(self, request, pk=None):
        return copy_titles_to_product(request, pk)
