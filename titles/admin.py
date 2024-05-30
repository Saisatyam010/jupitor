from django.contrib import admin
from .models import Title

@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'serial_number', 'title_name', 'prompt', 'product', 'created_at', 'modified_at')
    search_fields = ('title_name', 'prompt__prompt_text', 'product__name')
    list_filter = ('created_at', 'modified_at')
