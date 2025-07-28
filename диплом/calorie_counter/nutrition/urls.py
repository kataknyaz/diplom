from django.urls import path
from .views import (
    home, register, user_login, user_logout,
    product_list, add_product, delete_product,
    add_consumed_product, daily_stats
)

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('products/', product_list, name='product_list'),
    path('products/add/', add_product, name='add_product'),
    path('product/delete/<int:product_id>/', delete_product, name='delete_product'),
    path('consumed/add/', add_consumed_product, name='add_consumed_product'),
    path('stats/', daily_stats, name='daily_stats'),
]