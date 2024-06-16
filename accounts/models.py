from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager
# Create your models here.

# customer user admin

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254,unique=True)
    phone_number = models.CharField(max_length=50)

    #required
    date_joined = models.DateField(auto_now_add=True)
    last_login = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FEILD = 'email'
    REQUIRED_FIELDS = ['username','first_name', 'last_name', 'phone_number']


    def __str__(self):
        return self.email

    def has_perm (self , perms, obj_None):
        return self.is_admin
    
    def has_module_perms(self,add_label):
        return True