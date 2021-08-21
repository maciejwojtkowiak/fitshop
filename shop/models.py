from django.db import models


class Item(models.Model):
    title = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='pictures', default='static/images/man.png')

