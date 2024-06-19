from django.db import models
from category.models import Category
from django.urls import reverse


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

    def get_url(self):
        return reverse('product_details',args=[self.category.slug,self.slug])
    
class Meta:
    verbose_name = 'Product'
    verbose_name_plural = 'Products'

class VariationManger(models.Manager):
    def color(self):
        return super(VariationManger,self).filter(variation_category='color',is_active=True)
    
    def size(self):
        return super(VariationManger,self).filter(variation_category='size',is_active=True)

VARIATION_CATEGORY_CHOICE = {
    ('color', 'color'),
    ('size', 'size'),
    }
class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=VARIATION_CATEGORY_CHOICE)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    objects = VariationManger()


    def __str__(self):
        return self.product
