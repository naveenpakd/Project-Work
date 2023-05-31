from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Product(models.Model):
    name=models.CharField(max_length=180, null=False, blank=False)
    product_image=models.ImageField(upload_to="imagess", null=False, blank=False)
    description=models.CharField(max_length=1000, null=False, blank=False)
    quntity=models.IntegerField(null=False, blank=False)
    price=models.FloatField(null=False, blank=False)
   
    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
     
   
    
    @property
    def total_cost(self):
        return self.quantity * self.product.price
    
    def __str__(self):
        return f"Cart: {self.user.username} - {self.product.name}"
