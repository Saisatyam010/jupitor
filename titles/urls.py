from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TitleViewSet

router = DefaultRouter()
router.register(r'titles', TitleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
