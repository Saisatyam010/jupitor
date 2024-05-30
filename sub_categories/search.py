# sub_categories/search.py

from rest_framework.filters import SearchFilter

class SubCategorySearchFilter(SearchFilter):
    search_param = 'search'
