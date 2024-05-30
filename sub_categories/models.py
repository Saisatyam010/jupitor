# sub_categories/models.py
from django.db import models
from categories.models import Category

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    serial_number = models.PositiveIntegerField(unique=True, blank=True, null=True)
    product_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.serial_number:
            last_subcategory = SubCategory.objects.order_by('serial_number').last()
            if last_subcategory:
                self.serial_number = last_subcategory.serial_number + 1
            else:
                self.serial_number = 1
        super(SubCategory, self).save(*args, **kwargs)
        self.category.subcategory_count = self.category.subcategories.count()
        self.category.save()

    def delete(self, *args, **kwargs):
        category = self.category
        super(SubCategory, self).delete(*args, **kwargs)
        category.subcategory_count = category.subcategories.count()
        category.save()

    def __str__(self):
        return self.name
