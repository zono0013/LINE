from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name    = "chat"
urlpatterns = [
    path('chat/', views.chat, name="chat_rooms"),
    path('', views.loginview, name='login'),
    path('create/', views.create_login, name="create"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout")
]