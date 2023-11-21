from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.signin, name='login'),
    path('signup/', views.get_signup, name='signup'),
    path('lectures/', views.get_lectures, name='lectures'),
    path('book/', views.get_book, name='book'),
    #path('accounts/', include('django.contrib.auth.urls'))
]

