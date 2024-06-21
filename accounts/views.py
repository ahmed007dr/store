from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  
            user.username = user.email.split('@')[0]  
            user.date_joined = timezone.now()  
            user.save()  

            messages.success(request, 'Registration successful')
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
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('home')  # Replace 'home' with your desired redirect URL after login
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')  # Redirect back to login page with error message

    return render(request, 'accounts/login.html')


# def login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
#         user = authenticate(request, email=email, password=password)
        
#         if user is not None:
#             login(request, user)
#             messages.success(request, 'You are now logged in.')
#             return redirect('home')  # Redirect to home page after successful login
#         else:
#             messages.error(request, 'Invalid email or password.')
#             return redirect('login')  # Redirect back to login page if authentication fails
    
#     return render(request, 'accounts/login.html')


def loggout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')  
