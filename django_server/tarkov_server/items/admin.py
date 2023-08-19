from django.contrib import admin
from .models import *

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'ip', 'pay_date',
                    'use_date', 'verification',
                    'token']

admin.site.register(Profile, ProfileAdmin)
