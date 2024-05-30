# sub_categories/urls.py
from rest_framework.routers import DefaultRouter
from .views import SubCategoryViewSet

router = DefaultRouter()
router.register(r'sub_categories', SubCategoryViewSet)

urlpatterns = router.urls
