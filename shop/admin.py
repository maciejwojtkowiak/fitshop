from django.contrib import admin
from .models import Item, Profile, Comment, OrderItem, Order

admin.site.register(Item)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(OrderItem)
admin.site.register(Order)

