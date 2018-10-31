from django.contrib import admin
from django.urls import path
from DjApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'login', views.login),
    path(r'updateCheck/<djName>',views.checkUpDate),
    path(r'user/main',views.logInConformation),
    path(r'user/addSong', views.addSong),
    path(r'user/MainAction',views.mainAction),
    path(r'election/<djName>',views.userPage),
    path(r'electionsInAction/<elections_id>',views.electionInAction),
    path(r'vote',views.vote),
    path(r'finishElections',views.finishElectionDj)
]
