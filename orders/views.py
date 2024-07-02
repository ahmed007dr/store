from django.shortcuts import render ,redirect
from carts.models import CartItem 
from .forms import OrderForm 
import datetime
from .models import Order
# Create your views here.

    # # if the cart count is less than or equl to zero , then redirect baack to shop

def place_order(request, total = 0 , quantity = 0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total = (cart_item.product.price * cart_item.quantity)
        
        quantity += cart_item.quantity
        tax = (14 * total) / 100
        grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)  
        if form.is_valid():
            # store the order in database
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone_number = form.cleaned_data['phone_number']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.status = form.cleaned_data['status']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # genertion order number 
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime('%Y%m%d') # 2024 07 03
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            return redirect('checkout')
    else:
        form = OrderForm()

    # #return render(request, 'place_order.html')