"""
A module for admin
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.contrib import admin

# Internal
from .models import Contact
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Admin Class for Contact Model
    """
    list_display = (
        'name',
        'message',
        'phone',
        'email'
        )
    list_filter = (
        'name',
        'email'
        )
    search_fields = (
        'name','email',
        )