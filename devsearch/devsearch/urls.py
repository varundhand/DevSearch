from django.contrib import admin
from django.urls import path, include 

#making a math to access the images in our project
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',include('users.urls')),
    path('projects/', include('projects.urls')),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) #grabbing media url and connecting to media root where the image is uploaded
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)