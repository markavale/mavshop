from django.urls import path
from .views import index, cart_view

app_name = 'pages'

urlpatterns = [
    path('', index, name='index'),
    path('shopping-cart/', cart_view, name='shopping-cart')
]
