from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .forms import ImageCreateForm
from .models import Image


# Create your views here.

"""
View to store the images to the site
"""
@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST) # form is sent
        if form.is_valid():
            cd = form.cleaned_data # form data is valid
            new_image = form.save(commit=False)
            new_image.user = request.user # assign current user to the item
            new_image.save()
            messages.success(request, 'Image is added successfully')
            return redirect(new_image.get_absolute_url()) # redirect to the new created item detail view
    else:
        form = ImageCreateForm(data=request.GET) # build form with data provided by the bookmarklet via GET
    return render(
        request,
        'images/image/create.html',
        {'section': 'images', 'form': form}
    )

"""
View to display an image
"""
def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(
        request,
        'images/image/detail.html',
        {'section': 'images', 'image': image}
    )