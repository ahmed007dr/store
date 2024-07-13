from django.shortcuts import render, redirect ,get_object_or_404 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm ,UserProfileForm ,UserForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str  
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from .models import Account ,UserProfile
from carts.models import Cart ,CartItem
from carts.views import _cart_id
import requests
from orders.models import Order ,OrderProduct
from django.http import HttpResponse



User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email.split('@')[0]  # Set username based on email
            user.is_active = False  # Initially set user as inactive until email is verified
            password = form.cleaned_data.get('password')  # Assuming your form has a 'password' field
            user.set_password(password)
            user.save()

            # Send activation email (uncomment and modify as needed)
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            messages.success(request, 'Please confirm your email address to complete the registration')
            return redirect('login')
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))  
                cart_items = CartItem.objects.filter(cart=cart)

                for item in cart_items:
                    item.user = user  # Associate each CartItem with the logged-in user
                    item.save()

            except Cart.DoesNotExist:
                pass  # Handle case where cart does not exist

            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('home')  # Redirect to home page after successful login
        
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')  # Redirect back to login page with error message

    return render(request, 'accounts/login.html')



@login_required(login_url='login')
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')  

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link.')
        return redirect('login')



def resend_verification_email(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_object_or_404(User, email=email)

            if user.is_active:
                messages.info(request, 'Your account is already active.')
            else:
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('accounts/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()

                messages.success(request, 'A new activation link has been sent to your email.')
            return redirect('login')  
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/resend_verification_email.html', {'form': form})

@login_required(login_url='login')
def dashbord(request):
    order = Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    order_count = order.count()

    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'order_count': order_count,
        'userprofile':userprofile,
    }

    return render (request,'accounts/dashbord.html',context)

@login_required(login_url='login')
def my_orders(request):
    order = Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    context = {
        'orders': order,
        }
    return render(request,'accounts/my_orders.html',context)


@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile,user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'userprofile':userprofile,
            }
    return render(request,'accounts/edit_profile.html',context)



def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email=email)

            # Generate and send password reset email
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            
            messages.success(request, 'Password reset link sent to your email address.')
            return redirect('login')  # Redirect to login page after sending email
        else:
            messages.error(request, 'This email does not exist.')
            return redirect('forgotpassword')  # Redirect back to forgot password form
        
    return render(request, 'accounts/forgotpassword.html')


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request,'please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request, 'Invalid token or link has expired')
        return redirect('login')
    
def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password :
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,' we are done successe')
            return redirect('login')
        else:
            messages.error(request,'password dont match ')
            return redirect('resetpassword')
    else:     
        return render (request,'accounts/resetpassword.html')
    
@login_required(login_url='login')
def changePassword(request):
    if request.method == 'POST':
        current_password = request.POST['current_password'] # name = HTML 
        new_password = request.POST['new_password'] # name = HTML 
        confirm_password = request.POST['confirm_password'] # name = HTML 

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password changed successfully')
                return redirect('changePassword')
            else:
                messages.error(request,'Current password is incorrect')
                return redirect('changePassword')
        else:
            messages.error(request,'New password and confirm password does not match')
        return redirect('changePassword')
    else:
        return render(request,'accounts/change_password.html')
    

@login_required(login_url='login')
def order_detail(request, order_id):
    try:
        order = Order.objects.get(order_number=order_id)
        order_detail = OrderProduct.objects.filter(order=order)
        subtotal = 0
        for i in order_detail :
            subtotal += i.product_price * i.quantity

    except Order.DoesNotExist:
        return HttpResponse("Order not found", status=404)

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal':subtotal,
    }
    return render(request, 'accounts/order_detail.html', context)



