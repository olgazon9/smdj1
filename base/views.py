from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User

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
