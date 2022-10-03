from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import handler404, handler500

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('clothes/', include('clothes.urls')),
    path('bag/', include('bag.urls')),
    path('checkout/', include('checkout.urls')),
    path('profile/', include('profiles.urls')),
    path('contact/', include('contact.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'summerfashions.views.handler404'
handler500 = 'summerfashions.views.handler500'
