from django.shortcuts import render
from .models import Clothes

# Create your views here.

def all_clothes(request):
    """ View to return all clothes, including sorting and search queries"""

    clothes = Clothes.objects.all()
    context = {
        'clothes': clothes,
    }
    return render(request, 'clothes/clothes.html', context)
