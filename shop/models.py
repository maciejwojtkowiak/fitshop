from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import DecimalField, IntegerField
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from PIL import Image
from decimal import Decimal
from django.db.models import F, Sum


class Visits(models.Model):
    visits = models.IntegerField(default=0)
    class Meta:
        abstract = True
class Item(Visits, models.Model):
    title = models.CharField(max_length=150)
    price =  models.IntegerField(default=1000)
    image = models.ImageField(upload_to='pictures', default='static/images/man.png')
    description = models.TextField(default="Item")
    visits = models.IntegerField(default=0)
   

    def save(self):
        super().save()
        img = Image.open(self.image.path)

        if img.height > 280 or img.width > 280:
            new_img = (280, 280)
            img.thumbnail(new_img)
            img.save(self.image.path)

    def real_price(self):
        return self.price / 100

    def real_price_with_sign(self):
        return f"{self.price / 100}€"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    user_image = models.ImageField(upload_to='pictures', default='pictures/man.png')

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.user_image.path)

        if img.height > 280 or img.width > 280:
            new_img = (280, 280)
            img.thumbnail(new_img)
            img.save(self.user_image.path)

class Comment(models.Model):
    content = models.TextField(default='')
    comment_item = models.ForeignKey(Item, on_delete=CASCADE)
    comment_user = models.ForeignKey(User, on_delete=CASCADE)

class OrderItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField(default=1)

    @property
    def total(self):
        total = self.item.price * self.quantity
        total = total / 100
        total = f"{total}€"
        return total 

class Cart(models.Model):
    order_user = models.OneToOneField(User, on_delete=CASCADE)
    ordered = models.BooleanField(default=False)
    total = models.IntegerField(default=0, help_text="100 = 1EUR")
    order_items = models.ManyToManyField(Item, related_name='carts', through=OrderItem )

    def real_total(self):
        return self.total / 100 

    def total_with_sign(self):
        return f"{self.total / 100}€"


    

    

    
