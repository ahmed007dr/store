import os
import django
# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

import random
from faker import Faker



from category.models import Category
from accounts.models import Account
from store.models import Product, Variation, ReviewRating

# Initialize Faker with Arabic locale
fake = Faker('ar_SA')

# def create_categories(num=5):
#     for _ in range(num):
#         Category.objects.create(
#             category_name=fake.word(),
#             slug=fake.slug(),
#             description=fake.text(max_nb_chars=100),
#             cat_image=fake.image_url()
#         )

# def create_accounts(num=10):
#     for _ in range(num):
#         Account.objects.create(
#             username=fake.user_name(),
#             email=fake.email(),
#             password=fake.password(),
#             # Add other required fields as needed
#         )

def create_products(num=10):
    categories = Category.objects.all()
    for _ in range(num):
        Product.objects.create(
            Product_name=fake.word(),
            slug=fake.slug(),
            description=fake.text(max_nb_chars=250),
            price=random.randint(10, 1000),
            image=fake.image_url(),
            stock=random.randint(0, 100),
            is_available=fake.boolean(),
            category=random.choice(categories)
        )

def create_variations(num=20):
    products = Product.objects.all()
    variation_categories = ['color', 'size']
    for _ in range(num):
        Variation.objects.create(
            product=random.choice(products),
            variation_category=random.choice(variation_categories),
            variation_value=fake.color_name() if random.choice(variation_categories) == 'color' else fake.word(),
            is_active=fake.boolean()
        )

# def create_reviews(num=30):
#     products = Product.objects.all()
#     accounts = Account.objects.all()
#     for _ in range(num):
#         ReviewRating.objects.create(
#             product=random.choice(products),
#             user=random.choice(accounts),
#             subject=fake.sentence(nb_words=6),
#             review=fake.text(max_nb_chars=200),
#             rating=random.uniform(1, 5),
#             ip=fake.ipv4(),
#             status=fake.boolean()
#         )

if __name__ == '__main__':
    # print("Creating Categories...")
    # create_categories()
    # print("Categories created!")

    # print("Creating Accounts...")
    # create_accounts()
    # print("Accounts created!")

    print("Creating Products...")
    create_products()
    print("Products created!")

    print("Creating Variations...")
    create_variations()
    print("Variations created!")

    # print("Creating Reviews...")
    # create_reviews()
    # print("Reviews created!")
