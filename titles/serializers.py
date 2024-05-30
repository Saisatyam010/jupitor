from rest_framework import serializers
from .models import Title

class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = [
            'id',
            'serial_number',
            'title_name',
            'prompt',
            'product',
            'created_at',
            'modified_at'
        ]
