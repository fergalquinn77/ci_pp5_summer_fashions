from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from clothes.models import Clothes, Sale

def bag_contents(request):

    bag_items = []
    total = 0
    item_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_data in bag.items():
        if isinstance(item_data, int):
            item = get_object_or_404(Clothes, pk=item_id)
            total += item_data * item.price
            item_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'item': item,
            })

        else:
            product = get_object_or_404(Clothes, pk=item_id)
            sale = Sale.objects.all()
            
            for size, quantity in item_data['items_by_size'].items():
                if product.on_sale:
                    total += quantity * product.price * (1-product.sale.percent_off/100)
                else:
                    total += quantity * product.price
                item_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total
    if request.user.is_anonymous:
        wish_count = None
    else:
        wish_count = request.user.wishlist.count()

    context = {
        'bag_items': bag_items,
        'total': total,
        'item_count': item_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
        'wish_count': wish_count,
    }

    return context