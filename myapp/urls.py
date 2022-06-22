from pathlib import Path
from django.contrib import admin
from django.urls import path
from . import views
app_name = 'myapp'
urlpatterns = [
     path('', views.index),
     path('products/' , views.products, name='products'),
     path('products/<int:pk>/', views.Product_detail_view.as_view(), name='product_details'),
     path('products/add', views.Product_create_view.as_view() , name='add_product'),
     path('products/update/<int:id>/', views.update_product , name='update_product'),
     path('products/delete/<int:pk>/', views.Product_delete.as_view() , name='delete_product'),
     path('products/mylistings', views.my_listings , name='my_listings'),
]
