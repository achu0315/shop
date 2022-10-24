from.models import cart,cartitem
from . views import _cart_id

def counter(request):
    item_count=0
    if 'admin' in request.path:
        return  {}
    else:
        try:
            carts=cart.objects.filter(cart_id=_cart_id(request))
            car_items=cartitem.objects.all().filter(cart=carts[:1])
            for cart_item in car_items:
                item_count += cart_item.quantity
        except cart.DoesNotExist:
            item_count=0
    return dict(item_count=item_count)