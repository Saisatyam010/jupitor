# categories/search.py
from rest_framework import filters

class CategorySearchFilter(filters.SearchFilter):
    search_param = 'search'
    search_fields = ['category_name']
