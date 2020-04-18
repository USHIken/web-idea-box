from django.urls import path

from . import views

urlpatterns = [
    path('', views.ContentList.as_view(), name='index'),
]