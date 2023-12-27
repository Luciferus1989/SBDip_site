from django.urls import path
from .views import login_view, logout_view, RegisterView
from django.contrib.auth.views import LogoutView

app_name = 'myauth'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register')
]
