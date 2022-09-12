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
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField()
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    wishlists = models.ManyToManyField(User, related_name='wishlist', blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Clothes'

class ItemReview(models.Model):
    """
    A model to allow users to leave a review for an item
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(Clothes, on_delete=models.CASCADE)
    review = models.TextField(max_length=250, null=False, blank=False)
    rating = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'),), default=0)
    review_time = models.DateTimeField(auto_now_add=True, null=True)
    review_time_ago = models.CharField(max_length=20, null=False, blank=False,)
    liked = models.BooleanField(default=False,)

    class Meta:
            get_latest_by = 'id'

    def save(self, *args, **kwargs):
        
        self.review_time = datetime.now(timezone.utc)
        self.review_time_since = ((datetime.now(timezone.utc)
                                - self.review_time).days)
        super().save(*args, **kwargs)


@receiver(post_save, sender=ItemReview)
def update_average_rating(sender, instance, created, **kwargs):
    """
    Update average rating each time a new rating is added
    """

    item = Clothes.objects.get(pk=instance.item.pk)
    item_reviews = ItemReview.objects.filter(item=item.id)
    num_reviews = ItemReview.objects.filter(
        item=instance.item.id).filter(rating__gte=0).count()
    ratings = []
    count = 0
    sum = 0
    if num_reviews != 0:
        for review in item_reviews:
            ratings.append(review.rating)
            sum += review.rating
            count += 1
        average_rating = sum/count
        item.rating = average_rating
        item.save()
    else:
        item.rating = 0


@receiver(post_delete, sender=ItemReview)
def update_average_rating_deleted(sender, instance, **kwargs):
    """
    Update rating when a review is deleted
    """
    item = Clothes.objects.get(pk=instance.item.pk)
    item_reviews = ItemReview.objects.filter(item=item.id)
    num_reviews = ItemReview.objects.filter(
        item=instance.item.id)
    num_reviews = num_reviews.filter(rating__gte=0).count()
    ratings = []
    count = 0
    sum = 0
    if num_reviews != 0:
        for review in item_reviews:
            ratings.append(review.rating)
            sum += review.rating
            count += 1
        average_rating = sum/count
        item.rating = average_rating
        item.save()
    else:
        item.rating = 0
