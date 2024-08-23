from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
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

@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({ 'status': 'ok'})
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})

"""
A view to retrieve all images from the database. If requested by the browser, the whole page will be rendered.
For Fetch API requests, we will only render the HTML with new images, and they will be appended to the existing HTML page.
"""
@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8) # paginator to paginate over the results, retrieving 8 images per page
    page = request.GET.get('page') # to get requested page number
    images_only = request.GET.get('images_only') # check if retrieve the whole page or just new images
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1) # display the first page if the requested page is not an integer
    except EmptyPage:
        if images_only:
            return HttpResponse('') # if AJAX request is out of range, return an empty page
        images = paginator.page(paginator.num_pages) # if page os out of range return the last page
    if images_only:
        return render(
            request,
            'images/image/list_images.html',
            {'section': 'images', 'images': images}
        )
    return render(
        request,
        'images/image/list.html',
        {'section': 'images', 'images': images}
    )
        