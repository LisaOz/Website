from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

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
        upload_to='users/%Y/%m/%d/', # store te relative path to the file in the related databaase field (year, month, day)
        blank=True  # photo is optional. if the value is empty, a blank string will be stored
    )

    def __str__(self):
        return f'Profile of {self.user.username}'

""" 
This is the Contact model  used for the user relationships. Contains the following fields: 
user_from (user who created relationship), user_to (user being followed) and created (time when relationship was created).
"""
class Contact(models.Model):
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='rel_from_set',
        on_delete=models.CASCADE
    )
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='rel_to_set',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['created']),
        ]
        ordering = ['-created']
    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'
        
# The field is added to User dynamically
user_model = get_user_model() # retrieve the user model with Django generic function
user_model.add_to_class(
    'following',
    models.ManyToManyField(
        'self',
        through=Contact, # intermediate model in the table for many_to_many relationship
        related_name='followers',
        symmetrical=False
    )
)