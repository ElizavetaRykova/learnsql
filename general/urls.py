from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

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
    path('search_topic/', views.search_topic, name='search_topic'),
    path('change_password/', views.change_password, name='change_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('files/', views.manage_files, name='manage_files'),

    # url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout')
    #path('accounts/', include('django.contrib.auth.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

