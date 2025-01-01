from django.contrib import admin
from .models import Profile

# Customizing Profile admin
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'image')
    search_fields = ('user__username',)  # Allows search by username
    ordering = ('user',)

# Registering the Profile model with the admin interface
admin.site.register(Profile, ProfileAdmin)
