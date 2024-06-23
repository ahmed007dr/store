from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('resend-verification-email/', views.resend_verification_email, name='resend_verification_email'),
    path('dashbord/', views.dashbord, name='dashbord'),
    path('', views.dashbord, name='dashbord'),

]
