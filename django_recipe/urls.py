from django.contrib import admin
from django.urls import path, include
# Imports for images
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('profile/', include('user_profile.urls')),
    path('recipe/', include('recipe.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
