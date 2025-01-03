from django.urls import path, include
from home import views

app_name = "home"

urlpatterns = [
    path('', views.home_page, name="homely"),
    path('profile/', views.profile_page, name="profile_page"),
    path('financial/', views.financial_page, name="financial"),
    path('combined/', views.cibilbank_form, name='cibilbank_form'),
    path('eligibility/', views.eligibility_check, name='eligibility_check'),
    path('personal/', views.personal, name="personal"),
]