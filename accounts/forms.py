from django import forms
from django.forms import ModelForm
from .models import Account

class RegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))
    conform_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat Password',
        'class': 'form-control',
    }))

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "phone_number", "email", "password"]

    def __init__(self, *args, **kwargs):  # Corrected initialization method name
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs['placeholder'] = 'Enter your first name'
        self.fields["last_name"].widget.attrs['placeholder'] = 'Enter your last name'
        self.fields["phone_number"].widget.attrs['placeholder'] = 'Enter your phone number'
        self.fields["email"].widget.attrs['placeholder'] = 'Enter your email'
        self.fields["password"].widget.attrs['placeholder'] = 'Enter your password'
        self.fields["conform_password"].widget.attrs['placeholder'] = 'Enter your confirm password'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        conform_password = cleaned_data.get("conform_password")

        if password != conform_password :
            raise forms.ValidationError("Password does not match!")
        else:
            return cleaned_data
        