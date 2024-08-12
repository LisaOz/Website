from django import forms
from django.contrib.auth import get_user_model
from .models import Profile


""" 
This is a form to authenticate the users against the database
"""
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput) # render the password HTML element so the browser treats as password input


"""
This is a model form for user model used for the registration on the website with username, real name and a password
"""
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label = 'Password',
        widget = forms.PasswordInput
    )
    password2 = forms.CharField(
        label = 'Repeat password',
        widget = forms.PasswordInput
    )


    """
    Method to ensure both entered passwords match
    """ 
    def clean_password2(self):
        cd =self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords do not match")
        return cd['password2']
    
    # Add validation to the email field that prevents users from registering  with the existing email
    def clean_email(self):
        data = self.cleaned_data['email'] # QuorySet to look up existing users with the same email address
        if User.objects.filter(email=data).exists(): # check for results
            raise forms.ValidationError('Email already registered')
        return data

    class Meta:
        model = get_user_model() # retrieve user model dynamically
        fields = ['username', 'first_name', 'email']


"""
Form to allow users to edit Django built-in attributes: first name, last name and email.
""" 
class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']

    """ 
    Method to prevent users from changing their email address to the existing email adddress of an existing user
    by excluding the current user from the query set
    """
    def clean_email(self):
        data = self.cleaned_data['email']
        sq = User.objects.exclude( # exclude the current address
            id = self.instance.id
        ).filter(
            email = data
        )
        if qs.exists():
            raise forms.ValidationError('Email already registered.')
        return data


"""
Form to allow users to edit the profile data that is saved to the custom Profile model: edit date of birth and photo 
""" 
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']