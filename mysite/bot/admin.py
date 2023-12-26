from django.contrib import admin
from .models import Profile
from .models import Message
from .forms import ProfileForm

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name')
    form = ProfileForm

@admin.register(Message)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'text', 'created_at', 'send')