from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from .forms import ImageCreateForm
from .models import Image
from actions.utils import create_action
import redis


# Create your views here.

 # Establish a Redis connection in order to use it in views

r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
    )

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
            create_action(request.user, 'bookmarked image', new_image)
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

    # Increment total image views by 1
    total_views = r.incr(f'image:{image.id}:views') # increment, store the final value in the total-views variable and pass it into template
    
    # Increment image ranking by 1. Zincrby() command is used  to store image views in a sorted set with the image:ranking key
    r.zincrby('image_ranking', 1, image.id)
    return render(
        request,
        'images/image/detail.html',
        {'section': 'images', 'image': image, 'total_views': total_views}
    )

""" 
A view to display the ranking of the most viewed images
"""
@login_required
def image_ranking(request):
    # Get image ranking dictionaty
    image_ranking = r.zrange(  # obtain the elements in the sorted set
        'image_ranking', 0, -1, # 0 -lowest score, -1 - highest score
        desc = True # retieve elements by descending score
    )[:10]  # get the fist 10 elements of the highest score
    image_ranking_ids = [int(id) for id in image_ranking]

    # Get most-viewed images. Bild a list of returned image ids and store it as a list of integers
    most_viewed = list(
        Image.objects.filter(
            id__in=image_ranking_ids

        )
    )
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(
        request,
        'images/image/ranking.html',
        {'section': 'images', 'most_viewed': most_viewed}
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
                create_action(request.user, 'likes', image)
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
        
   