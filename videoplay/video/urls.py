from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='video'),
    path('video/', views.index, name='video'),
    path('videoinfo/<int:id>', views.videoinfo, name='videoinfo'),
    path('play/<int:id>', views.videoplay, name='videoinfo'),
]