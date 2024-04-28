from django.test import TestCase
from django.contrib.auth.models import User
from app_authentication.forms import SignupForm,ChangePasswordForm

class SignupFormTestCase(TestCase):
    def setUp(self):
        self.initial_form_data={
            "username":"test_user",
            "email":"test@example.com",
            "password":"testpassword",
            "confirm_password":"testpassword",
        }
        self.form_data = self.initial_form_data

    def test_valid_form(self):
        form = SignupForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_wrong_password(self):
        self.form_data['confirm_password'] = "testpassword2" 
        form = SignupForm(data=self.form_data)
        self.form_data=self.initial_form_data
        self.assertFalse(form.is_valid())
        self.assertIn('password',form.errors)
        self.assertIn("Passwords do not match. Try again",form.errors['password'])

    def test_restricted_words_in_username(self):
        self.form_data['username'] = "authenticate" 
        form = SignupForm(data=self.form_data)
        self.form_data=self.initial_form_data
        self.assertFalse(form.is_valid())
        self.assertIn('username',form.errors)
        self.assertIn("Invalid name for user, this is a reserverd word.",form.errors['username'])

    def test_special_chars_in_username(self):
        self.form_data['username'] = "anique@123" 
        form = SignupForm(data=self.form_data)
        self.form_data=self.initial_form_data
        self.assertFalse(form.is_valid())
        self.assertIn('username',form.errors)
        self.assertIn("This is an Invalid user, Do not user these chars: @ , - , + ",form.errors['username'])

    def test_unique_username(self):
        # Create a user with a different email address
        User.objects.create_user(username=self.initial_form_data['username'],password=self.initial_form_data['password'],email="differentemail@example.com")
        # Now try to register with the same email as the existing user
        form = SignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username',form.errors)
        self.assertIn("User with this username already exists.",form.errors['username'])

    def test_unique_email(self):
        # Create a user with a different email address
        User.objects.create_user(username="different_username",password=self.initial_form_data['password'],email=self.initial_form_data['email'])
        # Now try to register with the same email as the existing user
        form = SignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email',form.errors)
        self.assertIn("User with this email already exists.",form.errors['email'])

class CleanPasswordFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',password="old_password")
        self.initial_data = {
            "id":self.user.id,
            "username":"testuser",
            "old_password":"old_password",
            "new_password":"new_password",
            "confirm_password":"new_password",
        }
        self.form_data=self.initial_data

    def test_valid_form(self):
        form = ChangePasswordForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_old_password(self):
        self.form_data['old_password']='incorrect_password'
        form = ChangePasswordForm(data=self.form_data)
        self.form_data=self.initial_data
        self.assertFalse(form.is_valid())
        self.assertIn("old_password",form.errors)
        self.assertIn("Old password do not match.",form.errors['old_password'])

    def test_invalid_confirm_password(self):
        self.form_data['confirm_password']='a different confirm password'
        form = ChangePasswordForm(data=self.form_data)
        self.form_data=self.initial_data
        self.assertFalse(form.is_valid())
        self.assertIn("new_password",form.errors)
        self.assertIn("Passwords do not match.",form.errors['new_password'])