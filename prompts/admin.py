from django.contrib import admin
from .models import Prompt

@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ('id', 'serial_number', 'product', 'created_at', 'modified_at', 'no_of_titles', 'times_generated', 'prompt_text')
    search_fields = ('prompt_text', 'product__name')
    list_filter = ('product',)
