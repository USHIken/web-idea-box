from django.urls import path

from main import views


app_name = 'main'

urlpatterns = [
    path('', views.ContentListView.as_view(), name='index'),
    path('list/<str:content_type>',
         views.ContentListByTypeView.as_view(), name='list_by_type'),
    path('create/', views.ContentCreateView.as_view(), name='create'),
    path('detail/<int:pk>', views.ContentDetailView.as_view(), name='detail'),
    path('update/<int:pk>', views.ContentUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', views.ContentDeleteView.as_view(), name='delete'),
    path('mentor/', views.mentor, name='mentor'),
]
