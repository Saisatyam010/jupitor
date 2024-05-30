from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.apps import apps
from .models import Product

@receiver(post_save, sender=Product)
def update_product_count_on_save(sender, instance, created, **kwargs):
    if created:
        instance.subcategory.product_count = instance.subcategory.products.count()
        instance.subcategory.save()

@receiver(post_delete, sender=Product)
def update_product_count_on_delete(sender, instance, **kwargs):
    instance.subcategory.product_count = instance.subcategory.products.count()
    instance.subcategory.save()

@receiver(post_save, sender=apps.get_model('prompts', 'Prompt'))
@receiver(post_delete, sender=apps.get_model('prompts', 'Prompt'))
def update_prompt_and_title_counts(sender, instance, **kwargs):
    product = instance.product
    Title = apps.get_model('titles', 'Title')
    product.no_of_prompts = product.prompts.count()
    product.title_count = sum(prompt.no_of_titles for prompt in product.prompts.all())
    product.save(update_fields=['no_of_prompts', 'title_count'])

@receiver(post_save, sender=apps.get_model('titles', 'Title'))
@receiver(post_delete, sender=apps.get_model('titles', 'Title'))
def update_title_counts(sender, instance, **kwargs):
    product = instance.product
    Title = apps.get_model('titles', 'Title')
    product.title_count = Title.objects.filter(prompt__product=product).count()
    product.save(update_fields=['title_count'])
