from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', include('users.api.v1.urls')),
    path('api/v1/telegram/', include('telegram.api.v1.urls')),
]
