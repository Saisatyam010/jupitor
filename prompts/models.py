from django.db import models
from django.apps import apps
from products.models import Product

class Prompt(models.Model):
    id = models.AutoField(primary_key=True)
    serial_number = models.IntegerField(default=0, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prompts')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    no_of_titles = models.PositiveIntegerField(default=0)
    prompt_text = models.TextField()
    title_name = models.JSONField(default=list, blank=True)  # Store title_name as a list
    times_generated = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.id:  # Only update serial number when creating a new prompt
            self.serial_number = self.product.prompts.count() + 1
        super().save(*args, **kwargs)
        self.product.no_of_prompts = self.product.prompts.count()
        Title = apps.get_model('titles', 'Title')
        self.product.title_count = Title.objects.filter(product=self.product).count()  # Correct title count
        self.product.save(update_fields=['no_of_prompts', 'title_count'])

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.product.no_of_prompts = self.product.prompts.count()
        Title = apps.get_model('titles', 'Title')
        self.product.title_count = Title.objects.filter(product=self.product).count()  # Correct title count
        self.product.save(update_fields=['no_of_prompts', 'title_count'])
        # Update serial numbers of remaining prompts
        prompts = Prompt.objects.filter(product=self.product).order_by('serial_number')
        for index, prompt in enumerate(prompts, start=1):
            prompt.serial_number = index
            prompt.save(update_fields=['serial_number'])

    def append_titles(self, new_titles):
        self.title_name.extend(new_titles)
        self.no_of_titles = len(self.title_name)
        self.save(update_fields=['title_name', 'no_of_titles'])
        Title = apps.get_model('titles', 'Title')
        self.product.title_count = Title.objects.filter(product=self.product).count()  # Correct title count
        self.product.save(update_fields=['title_count'])

    def __str__(self):
        return f'Prompt {self.serial_number} for Product {self.product.name}'
