from import_export import resources
from .models import Prompt

class PromptResource(resources.ModelResource):
    class Meta:
        model = Prompt
        fields = ('id', 'serial_number', 'product__name', 'created_at', 'modified_at', 'no_of_titles', 'times_generated', 'prompt_text')
