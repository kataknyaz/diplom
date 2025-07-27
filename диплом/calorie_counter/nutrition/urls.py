from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('stats/', views.daily_stats, name='daily_stats'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
]