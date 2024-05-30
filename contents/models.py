from django.db import models
from titles.models import Title
from products.models import Product


class Content(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='contents')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='contents')
    serial_number = models.PositiveIntegerField()
    objective = models.TextField()
    home_ingredients = models.TextField()
    box_ingredients = models.TextField()
    procedure = models.TextField()
    explanation = models.TextField()
    custom_command = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('title', 'product', 'serial_number')

    def save(self, *args, **kwargs):
        if not self.pk:
            max_serial = \
            Content.objects.filter(title=self.title, product=self.product).aggregate(models.Max('serial_number'))[
                'serial_number__max']
            self.serial_number = (max_serial or 0) + 1
        super().save(*args, **kwargs)
