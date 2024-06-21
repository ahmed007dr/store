from django.shortcuts import render ,redirect 
from store.models import Product
from .models import Cart ,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from store.models import Variation

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.create()
        cart = request.session.session_key  # Update cart after session creation
    return cart


def add_cart(request,product_id):
    product = Product.objects.get(id=product_id) # get the product 
    product_varition = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            
            try:
                varition = Variation.objects.get(product=product , variation_category__iexact=key,variation_value__iexact=value)
                product_varition.append(varition)
            except:
                pass



    try:
        
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    try :
        cart_item = CartItem.objects.get(product=product , cart=cart)
        if len(product_varition) > 0:
            cart_item.variations.clear()
            for item in product_varition:
                cart_item.variations.add(item)

        cart_item.quantity += 1 # if cart item already exists then increment the quantity
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1 ,
            cart = cart , 
        )
        if len(product_varition) > 0:
            cart_item.variations.clear()

            for item in product_varition:
                cart_item.variations.add(item)

        cart_item.save()
    return redirect('cart')


def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = Product.objects.get(id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except ObjectDoesNotExist:
        return HttpResponse('Product not found in cart')
    return redirect('cart')

def remove_cart_item(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = Product.objects.get(id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
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

        tax = (14 *total)/100
        grand_total = total + tax

        
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
        'tax':tax,
        'grand_total':grand_total,
    }
    
    return render(request, 'store/carts.html', context)


