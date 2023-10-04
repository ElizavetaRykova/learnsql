from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_signin, name='get_signin'),
    path('signup/', views.get_signup, name='signup'),
]
