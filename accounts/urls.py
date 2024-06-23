from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('resend-verification-email/', views.resend_verification_email, name='resend_verification_email'),
    # path('blog/', views.blog, name='blog'),
    # path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),

]
