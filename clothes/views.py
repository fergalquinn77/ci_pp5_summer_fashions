from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Clothes

# Create your views here.

def all_clothes(request):
    """ View to return all clothes, including sorting and search queries"""
    query = None
    clothes = Clothes.objects.all()
    
    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('clothes'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            clothes = clothes.filter(queries)
    
    
    context = {
        'clothes': clothes,
        'search_term': query,
    }
    return render(request, 'clothes/clothes.html', context)

def item_details(request, item_id):
    """ View to return detail on an item of clothes"""

    item = get_object_or_404(Clothes, pk=item_id)
    context = {
        'item': item,
    }
    return render(request, 'clothes/item_details.html', context)
