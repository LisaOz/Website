from django.db import models
from django.conf import settings

# Create your models here.

"""
User profile model
"""

class Profile(models.Model): # inherit from models.Model
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    
    date_of_birth = models.DateField(blank=True, null=True) # this field is optional
    photo = models.ImageField(
        upload_to='users/%Y/%m/%d/', # store te relative path to the file in the related databaase field
        blank=True  # photo is optional. if the value is empty, a blank string will be stored
    )

    def __str__(self):
        return f'Profile of {self.user.username}'