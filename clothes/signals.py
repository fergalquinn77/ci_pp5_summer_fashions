from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Sale

@receiver(post_save, sender=Sale)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.clothes.discounted_price()
    