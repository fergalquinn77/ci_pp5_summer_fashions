from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_clothes, name='clothes'),
    path('<int:item_id>/', views.item_details, name='item_details'),
    path('add/', views.add_item, name='add_item'),
    path('edit/<int:item_id>/', views.edit_item, name='edit_item'),
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('togglewish/<int:item_id>/',
         views.toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
]
