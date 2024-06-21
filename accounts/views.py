from django.shortcuts import render , redirect
from .forms import RegistrationForm
from .models import Account
from django.utils import timezone  # Import timezone to set date_joined
from django.contrib import messages
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Extract cleaned data from the form
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Create a new Account object
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                username=email.split('@')[0],
                phone_number=phone_number,
                date_joined=timezone.now()  # Set date_joined to current time
            )
            user.save()
            messages.success (request,'registerion successful')
            return redirect('register')
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    return render(request, 'accounts/login.html')

def loggout(request):
    return 
