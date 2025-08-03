from django.urls import path
from .views import HomeView, ProductListView, CartView, AddToCartView, SellerOrdersView, SubmitOrderView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add-to-cart'),
    path('submit-order/', SubmitOrderView.as_view(), name='submit-order'),
      path('seller/orders/', SellerOrdersView.as_view(), name='seller-orders'),
]
