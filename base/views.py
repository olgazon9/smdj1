from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Order, OrderDetails
from .serializers import ProductSerializer, OrderDetailsSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework import status


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, OrderDetails, Product

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_data = request.data

        # Create a new order and associate it with the authenticated user
        order = Order.objects.create(user=request.user)

        # Process each item in the cart and create OrderDetails for each item
        order_details = []
        for product_id, item in cart_data.items():
            try:
                product = Product.objects.get(id=int(product_id))
            except (ValueError, Product.DoesNotExist):
                return Response({'message': f'Product with ID {product_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            quantity = item.get('quantity', 1)
            price = product.price

            # Calculate the total price for this item
            total_price = price * quantity

            # Create an OrderDetails instance for the current item
            order_detail = OrderDetails(order=order, product_name=product.name, quantity=quantity, price=price)
            order_detail.save()  # Save the order detail to the database
            order_details.append(order_detail)

            return Response({'message': 'Checkout successful', 'username': request.user.username}, status=status.HTTP_201_CREATED)




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
 
        # Add custom claims
        token['username'] = user.username
        # ...
 
        return token
 
 
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ProductList(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def members(req):
    return HttpResponse("members only")

@api_view(["POST"])
def user_register(request):
    data = request.data  # Access the data sent in the POST request

    # Check if 'username' and 'password' fields are present in the data
    if 'username' in data and 'password' in data:
        username = data['username']
        password = data['password']

        # Check if the username is already in use
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already in use."}, status=400)

        # Create the user
        user = User.objects.create_user(username=username, password=password)
        return Response({"user": "created"})
    else:
        # Handle the case where 'username' or 'password' is missing
        return Response({"error": "Username and password are required fields."}, status=400)
