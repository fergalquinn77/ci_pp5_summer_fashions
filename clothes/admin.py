from django.contrib import admin
from .models import Clothes, Category


class ClothesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    ordering = ('name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

admin.site.register(Clothes, ClothesAdmin)
admin.site.register(Category, CategoryAdmin)
