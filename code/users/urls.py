from django.urls import path
from . import views


app_name = 'users'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('password/change/',
         views.UserPasswordChangeView.as_view(), name='password_change'),
    path('profile/<uuid:pk>/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='update'),
]
