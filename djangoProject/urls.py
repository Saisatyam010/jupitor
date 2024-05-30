from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('categories.urls')),
    path('api/', include('sub_categories.urls')),
    path('api/', include('products.urls')),
    path('api/', include('prompts.urls')),
    path('api/', include('titles.urls')),
    path('api/', include('contents.urls')),

]
