from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_clothes, name='clothes'),
    path('<item_id>/', views.item_details, name='item_details'),
]