from rest_framework import status
from rest_framework.response import Response
from .models import Title
from prompts.models import Prompt
from products.models import Product

def bulk_delete_titles(request):
    ids = request.data.get('ids', [])
    if not ids:
        return Response({'error': 'No IDs provided'}, status=status.HTTP_400_BAD_REQUEST)

    titles = Title.objects.filter(id__in=ids)
    products_to_update = set(title.product_id for title in titles)
    prompts_to_update = set(title.prompt_id for title in titles)
    titles.delete()

    for product_id in products_to_update:
        update_product_title_serial_numbers(product_id)

    for prompt_id in prompts_to_update:
        update_related_tables(prompt_id)

    return Response({'status': 'Titles deleted successfully'}, status=status.HTTP_200_OK)

def bulk_copy_titles_to_products(request):
    ids = request.data.get('ids', [])
    new_product_id = request.data.get('product_id')
    if not ids or not new_product_id:
        return Response({'error': 'No IDs or product ID provided'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        new_product = Product.objects.get(id=new_product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    titles = Title.objects.filter(id__in=ids)
    for title in titles:
        title.pk = None  # Set the primary key to None to create a new instance
        title.product = new_product
        title.save()

    update_product_title_serial_numbers(new_product.id)
    return Response({'status': 'Titles copied successfully'}, status=status.HTTP_200_OK)

def copy_titles_to_product(request, pk=None):
    new_product_id = request.data.get('product_id')
    if not new_product_id:
        return Response({'error': 'No product ID provided'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        title = Title.objects.get(pk=pk)
        new_product = Product.objects.get(id=new_product_id)
    except (Title.DoesNotExist, Product.DoesNotExist):
        return Response({'error': 'Title or product not found'}, status=status.HTTP_404_NOT_FOUND)

    title.pk = None  # Set the primary key to None to create a new instance
    title.product = new_product
    title.save()

    update_product_title_serial_numbers(new_product.id)
    return Response({'status': 'Title copied successfully'}, status=status.HTTP_200_OK)

def update_related_tables(prompt_id):
    prompt = Prompt.objects.get(id=prompt_id)
    prompt.no_of_titles = prompt.prompt_titles.count()
    prompt.title_name = "; ".join([title.title_name for title in prompt.prompt_titles.all()])
    prompt.save(update_fields=['no_of_titles', 'title_name'])

    # Update the title count in the product as well
    product = prompt.product
    product.title_count = Title.objects.filter(product=product).count()
    product.save(update_fields=['title_count'])

def update_product_title_serial_numbers(product_id):
    titles = Title.objects.filter(product_id=product_id).order_by('serial_number')
    for index, title in enumerate(titles, start=1):
        title.serial_number = index
        title.save(update_fields=['serial_number'])

def update_product_title_count(product_id):
    product = Product.objects.get(id=product_id)
    product.title_count = Title.objects.filter(product=product).count()
    product.save(update_fields=['title_count'])
