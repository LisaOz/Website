import requests
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django import forms
from .models import Image

"""
Define a ModelForm form from the Image model with three fields
"""
class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widgets = {
            'url': forms.HiddenInput, # this field will not be visible to users   
        }

    """
    Method to clean the url field by splitting the url to see if it has a valid extension
    """
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError(
                'This URL does not match valid image extensions.'
            )
        return url

    """
    Override the save() method to retrieve the image file by its URL
    """
    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False) # new Image instance is created
        image_url = self.cleaned_data['url'] # URL of the image is retrieved from the cleaned_data dictionary of the form
        name = slugify(image.title) # the image name is generated by combining the image title slug with the original file extension of the image
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'

        response = requests.get(image_url) # download image from the givem URL
        image.image.save(
            image_name,
            ContentFile(response.content),
            save=False
        )
        if commit:
            image.save()
        return image