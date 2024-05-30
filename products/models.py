from django.db import models
from sub_categories.models import SubCategory

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    serial_number = models.IntegerField(default=0, editable=False)
    name = models.CharField(max_length=255)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')
    title_count = models.IntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    short_desc = models.CharField(max_length=255, blank=True)
    long_desc = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    mrp_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    images = models.JSONField(default=list, blank=True)
    no_of_prompts = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.id:  # Only update serial number when creating a new product
            last_product = Product.objects.all().order_by('-serial_number').first()
            if last_product:
                self.serial_number = last_product.serial_number + 1
            else:
                self.serial_number = 1
        super().save(*args, **kwargs)
        self.subcategory.product_count = self.subcategory.products.count()
        self.subcategory.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.subcategory.product_count = self.subcategory.products.count()
        self.subcategory.save()

    def __str__(self):
        return self.name
