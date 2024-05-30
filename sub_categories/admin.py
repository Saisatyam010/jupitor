# sub_categories/admin.py
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import SubCategory
from .resources import SubCategoryResource

class SubCategoryAdmin(ImportExportModelAdmin):
    resource_class = SubCategoryResource
    list_display = ('name', 'serial_number', 'product_count', 'category', 'created_at', 'modified_at')

admin.site.register(SubCategory, SubCategoryAdmin)
