from django.db import models
from djmoney.models.fields import MoneyField


class Item(models.Model):
    title = models.CharField(max_length=150)
    amount = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,
    )
    image = models.ImageField(upload_to='pictures', default='static/images/man.png')

