from django.db import models
from prompts.models import Prompt
from products.models import Product

class Title(models.Model):
    id = models.AutoField(primary_key=True)
    serial_number = models.IntegerField(default=0, editable=False)
    title_name = models.TextField()
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name='prompt_titles')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # Assign the next serial number in sequence
            last_title = Title.objects.filter(product=self.product).order_by('-serial_number').first()
            if last_title:
                self.serial_number = last_title.serial_number + 1
            else:
                self.serial_number = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        product_id = self.product_id
        super().delete(*args, **kwargs)
        # Update serial numbers of remaining titles
        titles = Title.objects.filter(product_id=product_id).order_by('serial_number')
        for index, title in enumerate(titles, start=1):
            title.serial_number = index
            title.save(update_fields=['serial_number'])

    def __str__(self):
        return self.title_name
