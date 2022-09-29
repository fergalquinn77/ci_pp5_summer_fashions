"""
A module for admin in the clothes app
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.contrib import admin
# Internal
from .models import Clothes, Category, Sale
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class ClothesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'rating',
        'image',
    )
    list_filter = ('on_sale',)
    ordering = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Clothes, ClothesAdmin)
admin.site.register(Category, CategoryAdmin)


# Sale Admin
@admin.register(Sale)
class Salesdmin(admin.ModelAdmin):
    list_display = ['clothes', 'percent_off', 'start_date', 'end_date']
    search_fields = ['clothes']
    list_filter = ('start_date', 'end_date')
