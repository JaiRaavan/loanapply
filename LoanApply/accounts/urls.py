from django.urls import path, include
from accounts import views

app_name = "accounts"

urlpatterns = [
    path('', views.signup, name="signup"),
    path('signin/',views.loginview, name="login"),
    path('logout/',views.loggedout, name="logout"),
]