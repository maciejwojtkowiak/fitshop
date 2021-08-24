from django.db import models
from django.db.models.deletion import CASCADE
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
    quantity = models.IntegerField(default=1)

    def save(self):
        super().save()
        img = Image.open(self.image.path)

        if img.height > 280 or img.width > 280:
            new_img = (280, 280)
            img.thumbnail(new_img)
            img.save(self.image.path)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    user_image = models.ImageField(upload_to='pictures', default='static/images/man.p')

    def __str__(self):
        return f"{self.user.username} Profile"

