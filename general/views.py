from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# from django.contrib.auth.forms import AuthenticationForm
from .forms import MyAuthenticationForm, RegisterForm
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.http import JsonResponse
from .models import *
import firebird.driver as fdb


# Форма входа
def signin(request):
    if request.method == 'POST':
        form = MyAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('topic_list/')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = MyAuthenticationForm()
    return render(request, './registration/login.html', {'form': form})

# Отрисовка HTML-шаблона страницы регистрации
def get_signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # получаем имя пользователя и пароль из формы
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # выполняем аутентификацию
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('topic_list/')
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form': form})

# Отрисовка HTML-шаблона страницы со списком тем
def get_topic_list(request):
    return render(request, 'topic_list.html')

# Отрисовка HTML-шаблона страницы учебника
def get_book(request):
    return render(request, 'book.html')

# Отрисовка HTML-шаблона страницы c заданием
def get_task(request):
    obj = Task.objects.all()
    number_task = obj[0].task_id
    task = obj[0].task_text
    reference_quary = obj[0].task_solution
    global REFERENCE_RESULT
    global TASK_POINTS
    TASK_POINTS = obj[0].task_max_points
    with fdb.connect(
        database=settings.RDB_CONF['database'], 
        user=settings.RDB_CONF['user'], 
        password=settings.RDB_CONF['password'], 
        charset=settings.RDB_CONF['charset']).cursor() as cur:
        cur.execute(reference_quary)
        REFERENCE_RESULT = cur.fetchall()
        cur.close()
    response = {
        "task" : task,
        "number_task": number_task,
        "results": REFERENCE_RESULT
    }
    return render(request, 'task.html', response)

def check_solution(request):
    sql_statement = request.POST.get('sql_statement')
    sql_statement = sql_statement.replace('\n', ' ')
    obj = Task.objects.all()
    reference_quary = obj[0].task_solution
    with fdb.connect(
        database=settings.RDB_CONF['database'], 
        user=settings.RDB_CONF['user'], 
        password=settings.RDB_CONF['password'], 
        charset=settings.RDB_CONF['charset']).cursor() as cur:
        cur.execute(sql_statement)
        result = cur.fetchall()
        cur.close()
    if REFERENCE_RESULT == result:
        equal = True

        id_user = Student.objects.get(username=request.user)
        id_task = Task.objects.get(task_id=1)

        p = Points(point=TASK_POINTS,task=id_task,auth_user=id_user,answer=sql_statement)
        p.save()

    else:
        equal = False

    response = {
        "result" : result,
        "equal": equal
    }

    return JsonResponse(data=response)

def get_table_data(request):
    selected_table = request.POST.get('selected_table')
    print(selected_table)
    with fdb.connect(
        database=settings.RDB_CONF['database'], 
        user=settings.RDB_CONF['user'], 
        password=settings.RDB_CONF['password'], 
        charset=settings.RDB_CONF['charset']).cursor() as cur:
        cur.execute(f'select * from {selected_table};')
        result = cur.fetchall()
        cur.close()
    
    response = {
        "result" : result
    }

    return JsonResponse(data=response)
            