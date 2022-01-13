from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from registration import views
urlpatterns = [
   path('regitro', views.SignupView.as_view(), name="registro"),
]
