from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_countries.fields import CountryField


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label='Country', null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()

# Model for dealing with support tickets borrowed from my PP4

STATUS = ((0, "Open"), (1, "Closed"))

class Support_Tickets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="SupportTickets")
    title = models.CharField(max_length=200, blank=False)
    query = models.TextField(blank=False)
    status = models.IntegerField(choices=STATUS, default=0)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    class Meta:
        verbose_name_plural = 'Support Tickets'

    def __str__(self):
        return self.title

# Model for dealing with messages relating to support tickets
class Tickets_Messages(models.Model):
    ticket = models.ForeignKey(Support_Tickets, on_delete=models.CASCADE,
                               related_name="Tickets")
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=False)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"Comment {self.message} by {self.user}"

    class Meta:
        verbose_name_plural = 'Support Responses'
