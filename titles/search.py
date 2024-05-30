from rest_framework import filters
from .models import Title

class TitleSearchFilter(filters.SearchFilter):
    search_param = 'q'

    def get_search_fields(self, view, request):
        return ['title_name', 'prompt__prompt_text', 'product__name']
