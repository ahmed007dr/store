from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg
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
    
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
        
    
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
        return f"{self.id} - {self.product} - {self.variation_value}"


class ReviewRating(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    subject = models.CharField(max_length=100,blank=True)
    review = models.TextField(max_length=500,blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20,blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
