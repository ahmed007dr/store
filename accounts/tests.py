from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class RegistrationTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')  # Adjust 'register' to match your URL name
        self.login_url = reverse('login')  # Adjust 'login' to match your URL name
        self.home_url = reverse('home')  # Adjust 'home' to match your URL name
        
    def test_registration(self):
        # Prepare POST data for registration
        registration_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'password': 'testpassword',
        }
        
        # Simulate POST request to register view
        response = self.client.post(self.register_url, registration_data)
        
        # Check if registration is successful
        self.assertEqual(response.status_code, 302)  # Should redirect after successful registration
        self.assertTrue(get_user_model().objects.filter(email='test@example.com').exists())  # Check if user exists in database
    
    # def test_login(self):
    #     # Create a test user for login testing
    #     User = get_user_model()
    #     user = User.objects.create_user(
    #         email='test@example.com',
    #         password='testpassword',
    #         first_name='Test',
    #         last_name='User',
    #         phone_number='1234567890',
    #     )
        
    #     # Prepare POST data for login
    #     login_data = {
    #         'email': 'test@example.com',
    #         'password': 'testpassword',
    #     }
        
    #     # Simulate POST request to login view
    #     response = self.client.post(self.login_url, login_data)
        
    #     # Check if login is successful
    #     self.assertRedirects(response, self.home_url, status_code=302, target_status_code=200)
    #     self.assertIn('_auth_user_id', self.client.session)  # Check if user is logged in
    
    # def test_logout(self):
    #     # Create and login a test user
    #     User = get_user_model()
    #     user = User.objects.create_user(
    #         email='test@example.com',
    #         password='testpassword',
    #         first_name='Test',
    #         last_name='User',
    #         phone_number='1234567890',
    #     )
    #     self.client.force_login(user)
        
    #     # Simulate GET request to logout view
    #     response = self.client.get(reverse('logout'))  # Assuming 'logout' is mapped correctly
        
    #     # Check if logout is successful
    #     self.assertRedirects(response, self.home_url, status_code=302, target_status_code=200)
    #     self.assertNotIn('_auth_user_id', self.client.session)  # Check if user is logged out
