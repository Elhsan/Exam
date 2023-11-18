from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.exceptions import ValidationError



class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Set the default user ID
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='img/')
    description = models.TextField()
    reviews = models.TextField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Check if 'image' attribute is not None
        if self.image:
            try:
                # Open the image file
                img = Image.open(self.image.path)

                # Set the desired width and height
                desired_width = 600
                desired_height = 400

                # Resize the image if it exceeds the desired dimensions
                if img.width > desired_width or img.height > desired_height:
                    output_size = (desired_width, desired_height)
                    img = img.resize(output_size)
                    img.save(self.image.path)

            except (FileNotFoundError, ValidationError) as e:
                print(f"Error processing image: {e}")

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"