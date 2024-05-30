from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Title
from prompts.models import Prompt

@receiver(post_save, sender=Title)
@receiver(post_delete, sender=Title)
def update_prompt_and_product_on_save(sender, instance, **kwargs):
    update_related_tables(instance.prompt_id)

def update_related_tables(prompt_id):
    prompt = Prompt.objects.get(id=prompt_id)
    prompt.no_of_titles = Title.objects.filter(prompt=prompt).count()
    prompt.title_name = "; ".join([title.title_name for title in Title.objects.filter(prompt=prompt)])
    prompt.save(update_fields=['no_of_titles', 'title_name'])

    # Update the title count in the product as well
    product = prompt.product
    product.title_count = Title.objects.filter(product=product).count()
    product.save(update_fields=['title_count'])
