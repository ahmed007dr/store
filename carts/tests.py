from django.test import TestCase, Client
from django.urls import reverse
from store.models import Product

class CartTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name='Test Product',
            price=10.00,
            description='Test Description'
        )
        # You may need to create variations and associate them with the product

    def test_add_to_cart(self):
        response = self.client.post(reverse('add_cart', args=[self.product.id]), {'variation_name': 'Size', 'variation_value': 'M'})
        self.assertEqual(response.status_code, 302)  # Check if redirected to cart page

        # Check if product is in the cart
        response = self.client.get(reverse('cart'))
        self.assertContains(response, 'Test Product')
    
    def test_remove_from_cart(self):
        # Add a product to the cart first
        response = self.client.post(reverse('add_cart', args=[self.product.id]), {'variation_name': 'Size', 'variation_value': 'M'})
        self.assertEqual(response.status_code, 302)  # Check if redirected to cart page
        
        # Now remove the product from the cart
        response = self.client.post(reverse('remove_cart', args=[self.product.id, 1]))  # Assuming cart_item_id is 1
        self.assertEqual(response.status_code, 302)  # Check if redirected to cart page
        
        # Check if product is no longer in the cart
        response = self.client.get(reverse('cart'))
        self.assertNotContains(response, 'Test Product')

    def test_cart_totals(self):
        # Add multiple items to the cart and verify totals
        response = self.client.post(reverse('add_cart', args=[self.product.id]), {'variation_name': 'Size', 'variation_value': 'M'})
        self.assertEqual(response.status_code, 302)  # Check if redirected to cart page
        
        # Add another item or change quantities and check totals
        # ...

        # Validate total, tax, and grand total calculations in the cart view
        response = self.client.get(reverse('cart'))
        self.assertContains(response, 'Total: $')  # Check if total is displayed
        self.assertContains(response, 'Tax: $')    # Check if tax is displayed
        self.assertContains(response, 'Grand Total: $')  # Check if grand total is displayed
