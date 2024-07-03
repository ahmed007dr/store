from django.shortcuts import get_object_or_404, redirect ,render
from store.models import Product,Variation
from .models import Cart ,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.create()
        cart = request.session.session_key  # Update cart after session creation
    return cart

def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_variations = []
    
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            print("POST data - Key:", key, "Value:", value)
            
            try:
                variation = Variation.objects.get(product=product, 
                                                  variation_category__iexact=key,
                                                  variation_value__iexact=value)
                product_variations.append(variation)
                print("Found variation:", variation)
            except Variation.DoesNotExist:
                print("Variation does not exist for key:", key, "value:", value)
                pass
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        print("Cart found:", cart)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        print("Cart created:", cart)
    
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    print("Cart item exists:", is_cart_item_exists)

    if is_cart_item_exists:
        cart_items = CartItem.objects.filter(product=product, cart=cart)
        print("Cart items:", cart_items)
        
        for cart_item in cart_items:
            existing_variations = list(cart_item.variations.all())
            print("Existing variations:", existing_variations)
            
            if existing_variations == product_variations:
                cart_item.quantity += 1
                cart_item.save()
                print("Updated cart item quantity:", cart_item.quantity)
                return redirect('cart')
        
        new_cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
        new_cart_item.variations.set(product_variations)
        new_cart_item.save()
        print("New cart item created with variations:", new_cart_item.variations.all())
    else:
        new_cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
        new_cart_item.variations.set(product_variations)
        new_cart_item.save()
        print("New cart item created with variations:", new_cart_item.variations.all())
    
    return redirect('cart')

def remove_cart(request, product_id, cart_item_id ):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = Product.objects.get(id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart , id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request,product_id,cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = Product.objects.get(id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart , id = cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0 , quantity=0 , cart_item = None):
    try:
        total = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (14 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        cart = None
        cart_items = None
        total = 0
        quantity = 0
        tax = 0
        grand_total = 0
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
    }
    
    return render(request, 'store/carts.html', context)


@login_required(login_url='login')
def checkout(request,total=0 , quantity=0 , cart_item = None ):
    try:
        total = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (14 * total) / 100
        grand_total = total + tax


        
    except ObjectDoesNotExist:
        cart = None
        cart_items = None
        total = 0
        quantity = 0
        tax = 0  # Assign a default value if ObjectDoesNotExist is raised
        grand_total = 0  # Assign a default value

    context = {
        'cart': cart,
        'cart_items': cart_items, 
        'total': total,
        'quantity': quantity,
        'tax':tax,
        'grand_total':grand_total,
    }
    
    return render(request,'store/checkout.html',context)