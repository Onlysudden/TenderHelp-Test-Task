from django.contrib import admin
from django.urls import path

from app.views import RegistryAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RegistryAPIView.as_view()),
]
