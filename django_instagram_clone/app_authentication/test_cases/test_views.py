from django.test import TestCase,Client
from django.urls import reverse
from django.contrib.auth.models import User
from app_authentication.forms import SignupForm
from django.contrib.auth import authenticate

class SignupViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse("signup")
        self.form_data = {
            "username":"testuser",
            "email":"test@example.com",
            "password":"password",
            "confirm_password":"password"
        }

    def test_get_signup_form(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"authentication/signup.html")
        self.assertIsInstance(response.context['form'],SignupForm)

    def test_post_valid_signup_form(self):
        response = self.client.post(self.signup_url,self.form_data)
        self.assertTrue(User.objects.filter(username=self.form_data['username']).exists())

        # Authenticate the user
        user = authenticate(username=self.form_data['username'],password=self.form_data['password'])
        self.assertIsNotNone(user)
        self.assertTrue(user.is_authenticated)

        # Log in the user
        login_successful = self.client.login(username=self.form_data['username'],password=self.form_data['password'])
        self.assertTrue(login_successful)

        # Now test that accessing the edit_profile view redirects to the correct location
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, 'authentication/edit_profile.html')