from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product
from category.models import Category
from carts.models import CartItem,Cart
from carts.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

def store(request, category_slug=None):
    categories = None
    products = None
    products_count = 0  

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)


        paginator = Paginator(products,3) #number of item in store page 
        page = request.GET.get('page')
        page_product = paginator.get_page(page)


        products_count = products.count()  
    else:
        products = Product.objects.filter(is_available=True).order_by('id')

        paginator = Paginator(products,6) #number of item in store page 
        page = request.GET.get('page')
        page_product = paginator.get_page(page)


        products_count = products.count()  

    context = {
        'products': page_product,
        'products_count': products_count,
    }

    return render(request, 'store/store.html', context)


def product_details(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug , slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()

        
    except Exception as e :
        raise e
    
    context = {
        'single_product' : single_product,
        'in_cart':in_cart,
        }
    

    return render ( request,'store/product_details.html',context)


def search(request):
    context = {}
    keyword = request.GET.get('keyword', None)

    if keyword:
        products = Product.objects.filter(Q(description__icontains=keyword) |
                                          Q(Product_name__icontains=keyword)
                                         ).order_by('-created_date')
        products_count = products.count()
    else:
        products = Product.objects.filter(is_available=True).order_by('id')
        products_count = products.count()

    context = {
        'products': products,
        'products_count': products_count,
        'keyword': keyword,  # Optionally pass keyword back to template for display
    }

    return render(request, 'store/store.html', context)


def checkout(request):
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
    
    return render(request,'store/checkout.html',context)