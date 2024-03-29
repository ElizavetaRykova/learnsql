from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.signin, name='login'),
    path('signup/', views.get_signup, name='signup'),
    path('topic_list/', views.get_topic_list, name='topic_list'),
    path('book/', views.get_book, name='book'),
    path('task/', views.get_task, name='task'),
    path('check_solution/', views.check_solution, name='check_solution'),
    path('get_table_data/', views.get_table_data, name='get_table_data'),
    #path('accounts/', include('django.contrib.auth.urls'))
]

