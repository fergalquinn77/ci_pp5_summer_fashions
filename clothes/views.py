from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.core.paginator import Paginator

from .forms import ProductForm
from .models import Clothes, Category


# Create your views here.

def all_clothes(request):
    """ View to return all clothes, including sorting and search queries"""
    query = None
    category = None
    sort = None
    direction = None
    
    clothes = Clothes.objects.all()
    
    if request.GET:

        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                clothes = clothes.annotate(lower_name = Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            clothes = clothes.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            clothes = clothes.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            print(query)
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('clothes'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            clothes = clothes.filter(queries)
    
    current_sorting = f'{sort}_{direction}'

    paginator = Paginator(clothes, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'clothes': clothes,
        'search_term': query,
        'current_sorting':current_sorting,
        'page_obj':page_obj,
    }
    return render(request, 'clothes/clothes.html', context)

def item_details(request, item_id):
    """ View to return detail on an item of clothes"""

    item = get_object_or_404(Clothes, pk=item_id)
    context = {
        'item': item,
    }
    return render(request, 'clothes/item_details.html', context)

def add_item(request):
    """ Add an item to the store """
    form = ProductForm()
    template = 'clothes/add_item.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

