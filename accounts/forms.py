from django import forms
from django.forms import ModelForm
from .models import Account

class RegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat Password',
        'class': 'form-control',
    }))

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "phone_number", "email", "password"]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs['placeholder'] = 'Enter your first name'
        self.fields["last_name"].widget.attrs['placeholder'] = 'Enter your last name'
        self.fields["phone_number"].widget.attrs['placeholder'] = 'Enter your phone number'
        self.fields["email"].widget.attrs['placeholder'] = 'Enter your email'
        self.fields["password"].widget.attrs['placeholder'] = 'Enter your password'
        self.fields["confirm_password"].widget.attrs['placeholder'] = 'Enter your confirm password'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data
