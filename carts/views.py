from django.shortcuts import render ,redirect
from store.models import Product
from .models import Cart ,CartItem
from django.core.exceptions import ObjectDoesNotExist


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.create()
        cart = request.session.session_key  # Update cart after session creation
    return cart


def add_cart(request,product_id):
    product = Product.objects.get(id=product_id) # get the product 
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    try :
        cart_item = CartItem.objects.get(product=product , cart=cart)
        cart_item.quantity += 1 # if cart item already exists then increment the quantity
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1 ,
            cart = cart ,

        )
        cart_item.save()
    return redirect('cart')



def cart(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        total = 0
        quantity = 0
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        
    except ObjectDoesNotExist:
        cart = None
        cart_items = None
        total = 0
        quantity = 0
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
    }
    
    return render(request, 'store/carts.html', context)