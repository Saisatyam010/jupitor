from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Title
from prompts.models import Prompt
from django.apps import apps

def update_related_tables(prompt_id):
    prompt = Prompt.objects.get(id=prompt_id)
    Title = apps.get_model('titles', 'Title')
    prompt.no_of_titles = Title.objects.filter(prompt=prompt).count()  # Correctly get the length of the titles list
    prompt.title_name = [title.title_name for title in Title.objects.filter(prompt=prompt)]
    prompt.save(update_fields=['no_of_titles', 'title_name'])

@receiver(post_save, sender=Title)
def update_prompt_and_product_on_save(sender, instance, **kwargs):
    update_related_tables(instance.prompt_id)

@receiver(post_delete, sender=Title)
def update_prompt_and_product_on_delete(sender, instance, **kwargs):
    update_related_tables(instance.prompt_id)
