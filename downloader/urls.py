from django.urls import path
from . import views

app_name = 'downloader'

urlpatterns = [
    path('', views.index, name='index'),
    path('download/', views.download_audio, name='download_audio'),
]