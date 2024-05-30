from rest_framework import status
from rest_framework.response import Response
from .models import Prompt

def bulk_delete_prompts(request):
    ids = request.data.get('ids', [])
    if not ids:
        return Response({'error': 'No IDs provided'}, status=status.HTTP_400_BAD_REQUEST)

    Prompt.objects.filter(id__in=ids).delete()
    return Response({'status': 'Prompts deleted successfully'}, status=status.HTTP_200_OK)

def bulk_update_prompts(request):
    ids = request.data.get('ids', [])
    updates = request.data.get('updates', {})
    if not ids or not updates:
        return Response({'error': 'No IDs or updates provided'}, status=status.HTTP_400_BAD_REQUEST)

    prompts = Prompt.objects.filter(id__in=ids)
    prompts.update(**updates)
    return Response({'status': 'Prompts updated successfully'}, status=status.HTTP_200_OK)
