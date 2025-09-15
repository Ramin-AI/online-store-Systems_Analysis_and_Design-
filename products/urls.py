from django.urls import path
from . import views

urlpatterns = [
    # Public views
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    
    # Admin views - more accessible paths
    path('products/manage/', views.admin_product_list, name='admin_product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),
]