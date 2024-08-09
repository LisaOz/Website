from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile

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
            messages.success(request, 'Changes saved successfully.')
            return redirect('dashboard')
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