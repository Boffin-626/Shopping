from django.db import models
from django.contrib.auth.models import User 

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name_plural = 'customer'

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'product'

    def __str__(self):
        return self.name 
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name_plural = 'order'

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False 
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems ])
        return total 
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'order item'

    @property
    def get_total(self):
        total = self.product.price * self.quantity 
        return total 

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    province = models.CharField(max_length=200, null=True)
    postal_code = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'shipping address'

    def __str__(self):
        return self.address



