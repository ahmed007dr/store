from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('loggout/', views.loggout, name='loggout'),
    # path('services/', views.services, name='services'),
    # path('portfolio/', views.portfolio, name='portfolio'),
    # path('blog/', views.blog, name='blog'),
    # path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),

]
