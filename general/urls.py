from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.get_home, name='home'),
    path('signin/', views.signin, name='login'),
    path('signup/', views.get_signup, name='signup'),
    path('topic_list/', views.get_topic_list, name='topic_list'),
    path('book/', views.get_book, name='book'),
    path('task/', views.get_task, name='task'),
    path('solutions/', views.get_solutions, name='solutions'),
    path('check_solution/', views.check_solution, name='check_solution'),
    path('get_table_data/', views.get_table_data, name='get_table_data'),
    path('add_answer/', views.add_answer, name='add_answer'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('add_question/', views.add_question, name='add_question'),
    path('view_answer/', views.view_answer, name='view_answer'),
    path('view_comment/', views.view_comment, name='view_comment'),
    path('search/', views.search, name='search'),
    path('change_password/', views.change_password, name='change_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    #path('accounts/', include('django.contrib.auth.urls'))
]

