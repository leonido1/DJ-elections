from django.contrib import admin
from django.urls import path
from DjApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'login', views.login),
    path(r'updateCheck',views.checkUpDate)
]
