"""
A module for clothes views
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.db.models.functions import Lower
from django.core.paginator import Paginator
from decimal import Decimal
# Internal
from .forms import ProductForm
from .models import Clothes, Category, Sale
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def all_clothes(request):
    """ View to return all clothes, including sorting and search queries"""
    query = None
    category = None
    sort = None
    direction = None

    clothes = Clothes.objects.all()
    sales = Sale.objects.all()

    for sale in sales:
        sale.sale_price = sale.clothes.price*(1-sale.percent_off/100)
        sale.save()

    if request.GET:

        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                clothes = clothes.annotate(lower_name=Lower('name'))
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

        if 'sale' in request.GET:
            clothes = clothes.filter(on_sale=True)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               "You didn't enter any search criteria!")
                return redirect(reverse('clothes'))
            A = Q(name__icontains=query)
            B = Q(description__icontains=query)
            queries = A | B
            clothes = clothes.filter(queries)

    current_sorting = f'{sort}_{direction}'

    paginator = Paginator(clothes, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'clothes': clothes,
        'sales': sales,
        'search_term': query,
        'current_sorting': current_sorting,
        'page_obj': page_obj,
    }
    return render(request, 'clothes/clothes.html', context)


# View item details
def item_details(request, item_id):
    """ View to return detail on an item of clothes"""

    item = get_object_or_404(Clothes, pk=item_id)
    context = {
        'item': item,
    }
    return render(request, 'clothes/item_details.html', context)


# Add item
@login_required
def add_item(request):
    """ Add an item to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added item!')
            return redirect(reverse('add_item'))
        else:
            messages.error(
                request, (f'Failed to add item. '
                          f'Please ensure the form is valid.'))
    else:
        form = ProductForm()

    template = 'clothes/add_item.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


# Edit item
@login_required
def edit_item(request, item_id):
    """ Edit an item in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    item = get_object_or_404(Clothes, pk=item_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated item!')
            return redirect(reverse('item_details', args=[item.id]))
        else:
            messages.error(request,
                           'Failed to update item. Please validate.')
    else:
        form = ProductForm(instance=item)
        messages.info(request, f'You are editing {item.name}')

    template = 'clothes/edit_item.html'
    context = {
        'form': form,
        'item': item,
    }

    return render(request, template, context)


# Delete Item
@login_required
def delete_item(request, item_id):
    """ Delete an item from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    item = get_object_or_404(Clothes, pk=item_id)
    item.delete()
    messages.success(request, 'Items deleted!')
    return redirect(reverse('clothes'))


# Toggle item wishlist
@login_required
def toggle_wishlist(request, item_id):

    item = get_object_or_404(Clothes, id=item_id)

    if item.wishlists.filter(id=request.user.id).exists():
        item.wishlists.remove(request.user)
        messages.info(request, f'{item.name} removed from wishlist')
    else:
        item.wishlists.add(request.user)
        messages.success(request, f'Added {item.name} to wishlist')

    return redirect(request.META['HTTP_REFERER'])


# view wishlist
@login_required
def view_wishlist(request):
    """ View to a users wishlist"""
    clothes = Clothes.objects.all()
    wishlist = []
    for item in clothes:
        if item.wishlists.filter(id=request.user.id).exists():
            wishlist.append(item)
    context = {
        'wishlist': wishlist,
    }
    return render(request, 'clothes/wishlist.html', context)


# # Add to wishlist
# @login_required
# def item_like(request, id):
#     """
#     Allows users to like or unlike items
#     """

#     try:
#         item = Clothes.objects.get(pk=id)
#         if request.method == 'POST':
#             if ItemReview.objects.filter(item=item,
#                                          user=request.user).exists():
#                 item_review = ItemReview.objects.get(
#                                                     item=item,
#                                                     user=request.user)
#                 if item_review.liked:
#                     item_review.liked = False
#                     item_review.save()
#                 else:
#                     item_review.liked = True
#                     item_review.save()
#             else:
#                 item_review = ItemReview(item=item,
#                                          user=request.user,
#                                          liked=True)
#                 item_review.save()

    # except Clothes.DoesNotExist:
    #     return render(request, 'home/404.html')

    # redirect_url = request.POST.get('redirect_url',
    #                                 '/clothes/clothes.html')
    # return redirect((redirect_url))


# Toggle Sale Staus

def toggle_sale_status(request, item_id):
    item = get_object_or_404(Clothes, id=item_id)
    if item.on_sale is True:
        item.on_sale = False
        messages.success(request, f'Changed {item.name} to general sale')
        item.save()
    else:
        item.on_sale = True
        messages.success(request, f'Changed {item.name} to on-sale')
        item.save()

    return redirect(request.META['HTTP_REFERER'])


# Update Sale percentage
@user_passes_test(lambda u: u.is_superuser)
def update_sale_rate(request, item_id):
    item = get_object_or_404(Clothes, id=item_id)
    sale = Sale.objects.filter(clothes=item)
    discount = None
    if 'discount' in request.POST:
        discount = float(request.POST['discount'])
    if sale.count() == 0:
        Sale.objects.create(clothes=item, percent_off=0, sale_price=item.price)
    item.sale.percent_off = discount
    item.sale.sale_price = item.price * Decimal(1 - discount/100)
    item.sale.save()
    return redirect(request.META['HTTP_REFERER'])
