from django.urls import path
from .views import CheckoutView, OrderDetailsView, OrderHistoryView, ProductList, MyTokenObtainPairView, members, user_register

urlpatterns = [
    path('products', ProductList.as_view(), name='product-list'),
    path('login/', MyTokenObtainPairView.as_view()),
    path('members/', members, name='members'),
    path('register/', user_register, name='register'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-history/', OrderHistoryView.as_view(), name='order-history'),
    path('order-details/', OrderDetailsView.as_view(), name='order-details'),

]
