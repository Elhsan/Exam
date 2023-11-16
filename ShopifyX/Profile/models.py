from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    interests = models.TextField(max_length=100)
    last_visit = models.DateTimeField(null=True, blank=True)
    visit_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username