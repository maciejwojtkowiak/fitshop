from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile, Cart

@receiver(post_save, sender=User)
def profile_creation(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Cart.objects.create(order_user=instance)

@receiver(post_save, sender=User)
def profile_creation(sender, instance, **kwargs):
        instance.profile.save()