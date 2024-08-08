from django import forms
from django.contrib.auth import get_user_model


""" 
This is a form to authenticate the users against the database
"""
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput) # render the password HTML element so the browser treats as password input


"""

A model form for user model used for the registration on the website with username, real name and a password
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

    class Meta:
        model = get_user_model() # retrieve user model dynamically
        fields = ['username', 'first_name', 'email']

    