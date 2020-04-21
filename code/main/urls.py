from django.urls import path

from main import views


app_name = 'main'

urlpatterns = [
    path('', views.ContentListView.as_view(), name='index'),
    path('create/', views.ContentCreateView.as_view(), name='create'),
    path('detail/<int:pk>', views.ContentDetailView.as_view(), name='detail'),
    path('update/<int:pk>', views.ContentUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', views.ContentDeleteView.as_view(), name='delete'),
]