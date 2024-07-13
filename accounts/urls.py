from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('resend-verification-email/', views.resend_verification_email, name='resend_verification_email'),
    path('dashbord/', views.dashbord, name='dashbord'),
    path('', views.dashbord, name='dashbord'),

    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('password_reset_confirm/<str:uidb64>/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
    path('my_orders/',views.my_orders,name="my_orders"),
    path('edit_profile/',views.edit_profile,name="edit_profile"),
    path('changePassword/',views.changePassword,name="changePassword"),
    # path('profile/', views.profile, name='profile'),

]
