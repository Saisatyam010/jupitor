from rest_framework import status
from rest_framework.response import Response
from .models import Product, SubCategory

def bulk_delete_products(request):
    ids = request.data.get('ids', [])
    if not ids:
        return Response({'error': 'No IDs provided'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        products = Product.objects.filter(id__in=ids)
        subcategories_to_update = set(product.subcategory_id for product in products)
        products.delete()
        for subcategory_id in subcategories_to_update:
            update_subcategory_product_serial_numbers(subcategory_id)
        return Response({'status': 'Products deleted successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

def bulk_copy_products(request):
    product_ids = request.data.get('product_ids', [])
    target_subcategory_id = request.data.get('subcategory_id')

    if not product_ids or not target_subcategory_id:
        return Response({'error': 'Product IDs and Subcategory ID are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        target_subcategory = SubCategory.objects.get(id=target_subcategory_id)
    except SubCategory.DoesNotExist:
        return Response({'error': 'Subcategory not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        products = Product.objects.filter(id__in=product_ids)
        last_product = Product.objects.all().order_by('-serial_number').first()
        next_serial_number = last_product.serial_number + 1 if last_product else 1

        for product in products:
            Product.objects.create(
                serial_number=next_serial_number,
                name=product.name,
                subcategory=target_subcategory,
                title_count=product.title_count,
                created_at=product.created_at,
                modified_at=product.modified_at,
                short_desc=product.short_desc,
                long_desc=product.long_desc,
                tags=product.tags,
                selling_price=product.selling_price,
                mrp_price=product.mrp_price,
                images=product.images,
                no_of_prompts=product.no_of_prompts
            )
            next_serial_number += 1

        return Response({'status': 'Products copied to target subcategory'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

def update_subcategory_product_serial_numbers(subcategory_id):
    products = Product.objects.filter(subcategory_id=subcategory_id).order_by('created_at')
    for index, product in enumerate(products, start=1):
        product.serial_number = index
        product.save(update_fields=['serial_number'])
