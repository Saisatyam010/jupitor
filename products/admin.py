from django.contrib import admin
from .models import Product
from sub_categories.models import SubCategory
from categories.models import Category
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter

class CategoryFilter(SimpleListFilter):
    title = _('category')
    parameter_name = 'subcategory__category'

    def lookups(self, request, model_admin):
        categories = Category.objects.all()
        return [(category.id, category.name) for category in categories]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(subcategory__category__id=self.value())
        return queryset

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'serial_number', 'name', 'subcategory', 'title_count', 'created_at', 'modified_at']
    search_fields = ['name', 'subcategory__name', 'subcategory__category__name']
    list_filter = ['subcategory__name', CategoryFilter]
