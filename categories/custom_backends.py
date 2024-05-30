# categories/custom_backends.py
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
from rest_framework.exceptions import ValidationError

class CustomDateFilterBackend(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        params = request.query_params

        # Process created_at_after and created_at_before
        created_at_after = params.get('created_at_after')
        created_at_before = params.get('created_at_before')

        if created_at_after:
            try:
                created_at_after = datetime.strptime(created_at_after, '%d-%m-%Y').strftime('%Y-%m-%d')
                queryset = queryset.filter(created_at__gte=created_at_after)
            except ValueError:
                raise ValidationError({'created_at_after': 'Enter a valid date.'})

        if created_at_before:
            try:
                created_at_before = datetime.strptime(created_at_before, '%d-%m-%Y').strftime('%Y-%m-%d')
                queryset = queryset.filter(created_at__lte=created_at_before)
            except ValueError:
                raise ValidationError({'created_at_before': 'Enter a valid date.'})

        return super().filter_queryset(request, queryset, view)
