import json
from django.http import HttpRequest
from rest_framework import status
from rest_framework.response import Response
from .models import SubCategory
from categories.models import Category


def bulk_copy_subcategories(request):
    # Ensure request is an instance of HttpRequest
    assert isinstance(request, HttpRequest), "The `request` argument must be an instance of `django.http.HttpRequest`."

    try:
        # Parse JSON data
        data = json.loads(request.body)
        category_ids = data.get('category_ids', [])
        subcategory_ids = data.get('subcategory_ids', [])
        single_subcategory_id = data.get('subcategory_id')  # Support single subcategory as well
    except json.JSONDecodeError:
        return Response({'error': 'Invalid JSON data'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if category_ids are provided
    if not category_ids:
        return Response({'error': 'Category IDs are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Validate subcategory_ids or single_subcategory_id
    if not subcategory_ids and not single_subcategory_id:
        return Response({'error': 'Subcategory IDs or a single Subcategory ID is required'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        target_categories = Category.objects.filter(id__in=category_ids)
        if not target_categories.exists():
            return Response({'error': 'No valid target categories found'}, status=status.HTTP_404_NOT_FOUND)

        # Initialize list for copied subcategories IDs
        copied_subcategories = []

        # Handle single subcategory copy
        if single_subcategory_id:
            try:
                subcategory = SubCategory.objects.get(id=single_subcategory_id)
            except SubCategory.DoesNotExist:
                return Response({'error': 'Subcategory not found'}, status=status.HTTP_404_NOT_FOUND)

            for target_category in target_categories:
                new_subcategory = SubCategory.objects.create(
                    name=subcategory.name,
                    category=target_category,
                    serial_number=None,  # Serial number will be auto-generated
                )
                copied_subcategories.append(new_subcategory.id)

                # Optionally, update subcategory count in the target category
                target_category.subcategory_count = target_category.subcategories.count()
                target_category.save()

        # Handle multiple subcategories copy
        if subcategory_ids:
            subcategories = SubCategory.objects.filter(id__in=subcategory_ids)
            if not subcategories.exists():
                return Response({'error': 'No valid subcategories found'}, status=status.HTTP_404_NOT_FOUND)

            for subcategory in subcategories:
                for target_category in target_categories:
                    new_subcategory = SubCategory.objects.create(
                        name=subcategory.name,
                        category=target_category,
                        serial_number=None,  # Serial number will be auto-generated
                    )
                    copied_subcategories.append(new_subcategory.id)

                    # Optionally, update subcategory count in the target category
                    target_category.subcategory_count = target_category.subcategories.count()
                    target_category.save()

        return Response(
            {'status': 'Subcategories copied to target categories', 'copied_subcategories': copied_subcategories},
            status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

def bulk_delete_subcategories(request):
    # Ensure request is an instance of HttpRequest
    assert isinstance(request, HttpRequest), "The `request` argument must be an instance of `django.http.HttpRequest`."

    try:
        # Parse JSON data
        data = json.loads(request.body)
        ids = data.get('ids')
    except json.JSONDecodeError:
        return Response({'error': 'Invalid JSON data'}, status=status.HTTP_400_BAD_REQUEST)

    if not ids:
        return Response({'error': 'No IDs provided'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        subcategories = SubCategory.objects.filter(id__in=ids)
        subcategories.delete()
        return Response({'status': 'Subcategories deleted successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)