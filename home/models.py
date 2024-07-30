from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import Sum

class Cart(models.Model):

    def get_cart_total(self):
        return CartItem.objects.filter(cart=self).aggregate(total=Sum('pizza__price'))['total']


class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True 

class PizzaCategory(BaseModel):
    category_name = models.CharField(max_length=100)

class Pizza(BaseModel):
    category = models.ForeignKey(PizzaCategory, on_delete=models.CASCADE, related_name="pizzas")
    pizza_name = models.CharField(max_length=100)
    images = models.ImageField(upload_to='pizza')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True) 

class Cart(BaseModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="carts")
    is_paid = models.BooleanField(default=False)


    def get_cart_total(self):
        return CartItem.objects.filter(cart=self).aggregate(total=Sum('pizza__price'))['total']

class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

 
    



