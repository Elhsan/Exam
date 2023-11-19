from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    interests = models.TextField(max_length=100)
    last_visit = models.DateTimeField(null=True, blank=True)
    visit_count = models.PositiveIntegerField(default=0)
    profile_image = models.ImageField(upload_to='img/')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Check if 'profile_image' attribute is not None
        if self.profile_image:
            try:
                # Open the image file
                img = Image.open(self.profile_image.path)

                # Set the desired width and height
                desired_width = 100
                desired_height = 100

                # Resize the image if it exceeds the desired dimensions
                if img.width > desired_width or img.height > desired_height:
                    output_size = (desired_width, desired_height)
                    img = img.resize(output_size)
                    img.save(self.profile_image.path)

            except (FileNotFoundError, ValidationError) as e:
                print(f"Error processing profile image: {e}")