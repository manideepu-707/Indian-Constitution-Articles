from django.urls import path
from . import views

urlpatterns=[
    path('',views.home, name='home'),
    path('articles/', views.articles, name='articles'),  # Articles page
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('contact/', views.contact, name='contact'),
    path('logout',views.logout,name='logout')
]