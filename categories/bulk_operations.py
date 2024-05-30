from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category

@api_view(['POST'])
def bulk_delete_categories(request):
    ids = request.data.get('ids', [])
    if not ids:
        return Response({'error': 'No IDs provided'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        categories = Category.objects.filter(id__in=ids)
        categories.delete()
        return Response({'status': 'Categories deleted successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
