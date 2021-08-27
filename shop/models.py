from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import IntegerField
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from PIL import Image


class Item(models.Model):
    title = models.CharField(max_length=150)
    price = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,
    )
    image = models.ImageField(upload_to='pictures', default='static/images/man.png')
    description = models.TextField(default="Item")

    def save(self):
        super().save()
        img = Image.open(self.image.path)

        if img.height > 280 or img.width > 280:
            new_img = (280, 280)
            img.thumbnail(new_img)
            img.save(self.image.path)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    user_image = models.ImageField(upload_to='pictures', default='pictures/man.png')

    def __str__(self):
        return f"{self.user.username} Profile"


class Comment(models.Model):
    content = models.TextField(default='')
    item = models.ForeignKey(Item, on_delete=CASCADE)
    comment_user = models.ForeignKey(User, on_delete=CASCADE)

class OrderItem(models.Model):
    order_item = models.ForeignKey(Item, on_delete=CASCADE, null=True)
    quantity = models.IntegerField(default=1)

class Order(models.Model):
    order_user = models.ForeignKey(User, on_delete=CASCADE)
    order_items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    total = models.DecimalField(default=0.00, decimal_places=2, max_digits=11)


    

