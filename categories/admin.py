# categories/admin.py
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Category
from .resources import CategoryResource

class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ('category_name', 'serial_number', 'subcategory_count', 'created_at', 'modified_at')

admin.site.register(Category, CategoryAdmin)
