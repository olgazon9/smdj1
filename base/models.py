from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=50,null=True,blank=True)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    image = models.ImageField(null=True,blank=True,default='/placeholder.png')

 
 
    def __str__(self):
           return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to the User model
    order_id = models.AutoField(primary_key=True)  # Order ID
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time the order was created

    def __str__(self):
        return f"Order ID: {self.order_id}, User: {self.user}, Created At: {self.created_at}"


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # ForeignKey to the Order model
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order: {self.order}, Product: {self.product_name}, Quantity: {self.quantity}, Price: {self.price}"
