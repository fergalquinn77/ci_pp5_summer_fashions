from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_clothes, name='clothes'),
    path('<int:item_id>/', views.item_details, name='item_details'),
    path('add/', views.add_item, name='add_item'),
    path('edit/<int:item_id>/', views.edit_item, name='edit_item'),
]