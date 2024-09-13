from django.contrib import admin
from .models import Action

# Register your models here.

"""
This is the Action model of the administration site
""" 

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ['user', 'verb', 'target', 'created']
    list_filter = ['created']
    search_fields = ['verb']
