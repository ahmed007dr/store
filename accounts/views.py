from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str  
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from .models import Account
from carts.models import Cart ,CartItem
from carts.views import _cart_id
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
                cart = Cart.objects.get(cart_id=_cart_id(request))  # Assuming _cart_id function is defined somewhere
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
    return render (request,'accounts/dashbord.html')

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