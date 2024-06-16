from django.db import models
from category.models import Category


# Create your models here.
class Product(models.Model):
    Product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=250)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Product_name

    @property
    def get_slug(self):
        return self.slug if self.slug else self.Product_name.lower().replace(' ', '-')

class Meta:
    verbose_name = 'Product'
    verbose_name_plural = 'Products'