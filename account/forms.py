from django import forms

""" 
This is a form to authenticate the users against the database
"""
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput) # render the password HTML element