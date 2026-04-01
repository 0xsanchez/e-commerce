from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:id>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('reviews/', views.ReviewCreateView.as_view(), name='review-create'),
    path('wishlist/', views.WishlistListCreateView.as_view(), name='wishlist'),
]