from django.db import models
from djmoney.models.fields import MoneyField
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

    def save(self):
        super().save()
        img = Image.open(self.image.path)

        if img.height > 280 or img.width > 280:
            new_img = (280, 280)
            img.thumbnail(new_img)
            img.save(self.image.path)

