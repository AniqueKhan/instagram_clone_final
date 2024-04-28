from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import os
from app_authentication.models import Profile

class ProfileModelTestCase(TestCase):
    def setUp(self):
        self.data={
            "username":"testuser",
            "password":"password"
        }
        self.user = User.objects.create_user(username=self.data['username'],password='password')

    def test_profile_creation(self):
        self.assertEqual(Profile.objects.count(),1)

    def test_profile_str(self):
        self.assertEqual(str(Profile.objects.get(user=self.user)),self.data['username'])

    def test_profile_picture_upload(self):
        profile = Profile.objects.get(user=self.user)

        # Create a test image file
        test_image = Image.new("RGB",(100,100))
        test_image_path='test_image.jpg'
        test_image.save(test_image_path)
        test_image_file=SimpleUploadedFile(name='test_image.jpg',content=open(test_image_path,'rb').read(),content_type="image/jpeg")

        # Set Image Profile
        profile.picture = test_image_file
        profile.save()

        # Check if the picture was saved successfully
        self.assertTrue(profile.picture)
        self.assertTrue(os.path.exists(profile.picture.path))

        # Clean up the test image file
        os.remove(test_image_path)