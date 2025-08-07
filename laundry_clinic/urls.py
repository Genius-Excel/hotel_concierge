
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('only-my-admin/', admin.site.urls),
    path('', include('base_app.urls')),
]
