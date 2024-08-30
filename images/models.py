from django.utils.text import slugify
from django.conf import settings
from django.db import models
from django.urls import reverse

# Create your models here.

"""
This is the model to store images in the platform
"""
class Image(models.Model):
    user = models.ForeignKey( # User object has many-to-one relationship
        settings.AUTH_USER_MODEL,
        related_name='images_created',
        on_delete=models.CASCADE # when the user is deleted the corresponding images are deleted
    )
    title = models.CharField(max_length=200)  # title for the image
    slug = models.SlugField(max_length=200, blank=True)  # letters, numbers, undescore and hyphens for SEO-friendly URLs
    url = models.URLField(max_length=2000)  # the original URL for the image
    image = models.ImageField(upload_to='images/%Y/%m/%d/')  # the image file
    description = models.TextField(blank=True)  # optional description of the image
    created = models.DateTimeField(auto_now_add=True)  # time and date when the object was created in the database, current datetime is set automatically
    total_likes = models.PositiveIntegerField(default=0)
    users_like = models.ManyToManyField( # create intermediary join table
        settings.AUTH_USER_MODEL,
        related_name='images_liked', # relationship from the related object to this 
        blank=True
    
    )


    """
    Class Meta for defining indexes and ordering
    """
    class Meta:
        indexes = [
            models.Index(fields=['created']),  # define a database index in descending order (indicated by hyphen) for the 'created' field
            models.Index(fields=['-total_likes']) # store the total number of users who like each image
        ]
        ordering = ['-created'] # the new images will be displayed first

    
    def __str__(self):
        return self.title

    """
    Method to automatically generate the slug field based on the value of the 'title' field
    """
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) 
        super().save(*args, **kwargs)
    
    """
    Method get_absolute_url(): method to the Image model, that is a common pattern for providing URLs for objects
    """
    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])



