from django.urls import path
from .views import ProductList, MyTokenObtainPairView, members, user_register, checkout

urlpatterns = [
    path('products/', ProductList.as_view(), name='product-list'),
    path('login/', MyTokenObtainPairView.as_view()),
    path('members/', members, name='members'),
    path('register/', user_register, name='register'),
    path('checkout/', checkout, name='checkout'),

]
