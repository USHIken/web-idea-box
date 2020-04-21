from django.urls import path

from main import views


app_name = 'main'

urlpatterns = [
    path('', views.ContentListView.as_view(), name='index'),
    path('detail/<int:pk>', views.ContentDetailView.as_view(), name='detail'),
    path('delete/<int:pk>', views.ContentDeleteView.as_view(), name='delete'),
]