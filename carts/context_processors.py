from .models import Cart , CartItem 
from .views import _cart_id


#number of cart items
def counter(request):
    cart_count = 0

    if 'admin' in request.path:
        return {}  # Return an empty dictionary for admin views
    else:
        try:
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            else:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart, is_active=True)

            for item in cart_items:
                cart_count += item.quantity

        except Cart.DoesNotExist:
            cart_count = 0
        except CartItem.DoesNotExist:
            cart_count = 0

    return {'cart_count': cart_count}
