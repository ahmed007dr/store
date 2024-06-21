from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class LoginTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')  # Adjust 'login' to match your URL name
    
    def test_valid_login(self):
        # Create a test user
        test_user = User.objects.create_user(email='test@example.com', password='testpassword')
        
        # Prepare POST data
        login_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        
        # Simulate POST request
        response = self.client.post(self.login_url, login_data)
        
        # Check if the user is logged in
        self.assertEqual(response.status_code, 302)  # Should redirect to 'home'
        self.assertTrue(response.url.endswith(reverse('home')))
        
        # You can also check if the success message is present in the messages
        self.assertContains(response, 'You are now logged in.', status_code=200)
        
    def test_invalid_login(self):
        # Prepare POST data with invalid credentials
        login_data = {
            'email': 'invalid@example.com',
            'password': 'invalidpassword',
        }
        
        # Simulate POST request
        response = self.client.post(self.login_url, login_data)
        
        # Check if it redirects back to the login page
        self.assertEqual(response.status_code, 302)  # Should redirect to 'login'
        self.assertTrue(response.url.endswith(reverse('login')))
        
        # Check if the error message is present in the messages
        self.assertContains(response, 'Invalid email or password.', status_code=200)

