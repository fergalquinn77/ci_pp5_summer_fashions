from django.shortcuts import render, get_object_or_404
from .models import Clothes

# Create your views here.

def all_clothes(request):
    """ View to return all clothes, including sorting and search queries"""

    clothes = Clothes.objects.all()
    context = {
        'clothes': clothes,
    }
    return render(request, 'clothes/clothes.html', context)

def item_details(request, item_id):
    """ View to return detail on an item of clothes"""

    item = get_object_or_404(Clothes, pk=item_id)
    context = {
        'item': item,
    }
    return render(request, 'clothes/item_details.html', context)
