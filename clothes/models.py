from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from datetime import datetime, timezone


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Clothes(models.Model):
    category = models.ForeignKey('Category', null=True,
                                 blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2,
                                 null=True, blank=True)
    stock = models.PositiveIntegerField()
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    wishlists = models.ManyToManyField(User,
                                       related_name='wishlist', blank=True)
    on_sale = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Clothes'


class Sale(models.Model):
    """
    A model to allow users to leave a review for an item
    """
    clothes = models.OneToOneField('Clothes', null=True,
                                   blank=True, on_delete=models.CASCADE)
    percent_off = models.DecimalField(max_digits=6,
                                      decimal_places=2, default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def discounted_price(self):
        """
        Update discounted price each time
        new discount applied
        """
        self.sale_price = self.price * (1 - self.percent_off/100)
        self.save()