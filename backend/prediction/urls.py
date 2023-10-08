from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('predict/',PredictionView.as_view(),name='predict'),







]

