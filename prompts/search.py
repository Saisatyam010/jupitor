from rest_framework import filters
from .models import Prompt

class PromptSearchFilter(filters.SearchFilter):
    search_param = 'q'

    def get_search_fields(self, view, request):
        return ['prompt_text', 'id', 'product__id']
