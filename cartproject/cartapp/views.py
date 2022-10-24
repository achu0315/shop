from django.shortcuts import render, redirect
from shop.models import product
from .models import cart, cartitem
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def _cart_id(request):
    Cart = request.session.session_key

    if not Cart:
        Cart = request.session.create()
    return Cart


def add_cart(request, product_id):
    products = product.objects.get(id=product_id)
    try:
        carts = cart.objects.get(cart_id=_cart_id(request))
    except cart.DoesNotExist:
        carts = cart.objects.create(
            cart_id=_cart_id(request)
        )
        carts.save(),
    try:
        cart_item = cartitem.objects.get(product=products, cart=carts)
        if cart_item.quantity < cart_item.product.stock:
             cart_item.quantity += 1
        cart_item.save()
    except cartitem.DoesNotExist:
        cart_item = cartitem.objects.create(
            product=products,
            quantity=1,
            cart=carts
        )
        cart_item.save()
    return redirect('cartapp:cart_detail')


def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        carts = cart.objects.get(cart_id=_cart_id(request))
        cart_items = cartitem.objects.filter(cart=carts, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request, 'cart.html', dict(cart_items=cart_items, total=total, counter=counter))
