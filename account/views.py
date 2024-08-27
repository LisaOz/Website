from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Contact, Profile

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('User authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

"""
Dashboard view; being displayed after check whether the user is authenticated, 
otherwise the user is redirected to the Login URL
"""
@login_required
def dashboard(request):
    return render(
        request,
        'account/dashboard.html',
        {'section': 'dashboard'}
    )

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False) # create user
            new_user.set_password( # method handles password hashing before storing the password in the database
                user_form.cleaned_data['password']
            )
            new_user.save() # save user
            Profile.objects.create(user=new_user) # Create user profile
            return render(
                request,
                'account/register_done.html', # display the form with the user registered template
                {'new_user': new_user}
            )
    else:
        user_form = UserRegistrationForm()
    return render(
        request,
        'account/register.html',
        {'user_form': user_form}
    )


""" 
This is an edit view to allow user to edit their details. 
"""
@login_required # For authenticated users only
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm( # to store the data of the built-in user model
            instance=request.user,
            data=request.POST
        )

        profile_form = ProfileEditForm( # to store the data of the custom Profile model
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )

        # if both forms contain valid data, both forms are saved to update the corresponding oblects in the database
        if user_form.is_valid() and profile_form.is_valid(): 
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile updated successfully.")
        else:
            messages.error(request, "Error updating your profile.") 
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    
    # Render the edit page with forms
    return render(
        request,
        'account/edit.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        }
    )


User = get_user_model() # Retrieve the User model dynamically

"""
List view for user object used to get all active users
"""
@login_required
def user_list(request):
    users = User.objects.filter(is_active=True) # flag is_active=True to retrieve only active users
    return render(
        request,
        'account/user/list.html',
        {'section': 'people', 'users': users}
    )

"""
Detail view for user object
"""
@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True) # retrive the active user with the given username
    return render(
        request,
        'account/user/detail.html',
        {'section': 'people', 'user': user}
    )


""" 
This is a user follow view
"""
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')

    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user
                )
            else:
                Contact.objects.filter(
                    user_from=request.user,
                    user_to=user
                ).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})