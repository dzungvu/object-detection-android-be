from django.urls import path
from .views import search_shop

urlpatterns = [
    path('', search_shop, name='search_shop'),
]