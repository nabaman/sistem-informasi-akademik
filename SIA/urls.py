
from django.urls import path,include
from django.contrib import admin
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView, name='index'),
    path('dashboard/',include('dashboard.urls', namespace='dashboard'))


]
