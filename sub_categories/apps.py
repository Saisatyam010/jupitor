# sub_categories/apps.py

from django.apps import AppConfig

class SubCategoriesConfig(AppConfig):
    name = 'sub_categories'

    def ready(self):
        import sub_categories.signals
