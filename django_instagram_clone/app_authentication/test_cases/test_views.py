from django.test import TestCase,Client
from django.urls import reverse
from django.contrib.auth.models import User
from app_authentication.forms import SignupForm,ChangePasswordForm
from app_authentication.models import Profile
from django.contrib.auth import authenticate
from post.models import Post

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

class PasswordChangeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='old_password')
        self.client.login(username='testuser', password='old_password')
        self.form_data = {
            'id':self.user.id,
            "old_password":"old_password",
            "new_password":"new_password",
            "confirm_password":"new_password"
        }

    def test_password_change_view_with_valid_data(self):
        # Simulate a post request with valid form data
        new_password = "new_password"
        response = self.client.post(reverse("password_change"),self.form_data)

        # Check if the users response has been updated
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))

        # Check if the view redirects to the password change done page
        self.assertRedirects(response, reverse('password_change_done'))

    def test_password_change_view_with_invalid_data(self):
        # Changing the value of the confirm password to raise errors
        self.form_data['confirm_password'] = "different password"
        response = self.client.post(reverse("password_change"),self.form_data)

        # Check if the form errors are displayed
        self.assertFormError(response,"form","new_password","Passwords do not match.")

    def test_password_change_view_get_request(self):
        # Simulate a GET request to the password change view
        response = self.client.get(reverse('password_change'))

        # Check if the correct template is rendered
        self.assertTemplateUsed(response, 'authentication/change_password.html')

        # Check if the form is passed to the context
        self.assertIsInstance(response.context['form'], ChangePasswordForm)

class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='old_password')
        self.profile = Profile.objects.filter(user=self.user).first()
        self.client.login(username='testuser', password='old_password')

    def test_profile_view(self):
        # Create a test post
        Post.objects.create(user=self.user,caption="Test caption")

        # Simulate a get request to the user's profile
        response = self.client.get(reverse("profile",args=[self.user.username]))

        # Check if the template used is correct or not
        self.assertTemplateUsed(response,"authentication/profile.html")

        # Check if the correct user profile is retrieved
        self.assertEqual(response.context['profile'], self.profile)

        # Check if the correct number of posts is passed to the context
        self.assertEqual(len(response.context['posts']), 1)

        # Check if the post count matches
        self.assertEqual(response.context['posts_count'], 1)

        # Check if the correct follow status is passed to the context
        self.assertEqual(response.context['follow_status'].count(), 0)

        # Check the context about followers and following information
        self.assertEqual(response.context['following_count'], 0)
        self.assertEqual(response.context['followers_count'], 0)