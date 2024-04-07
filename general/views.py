from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# from django.contrib.auth.forms import AuthenticationForm
from .forms import MyAuthenticationForm, RegisterForm
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.http import JsonResponse
from .models import *
import firebird.driver as fdb
from django.db.models import Sum


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
# <QuerySet [(1, 'Лекция 1'), (2, 'Лекция 2')]>
# [(1, "имя лекции", [(1, "задание"),(2, "задание")]),
#  (2, "имя лекции", [(3, "задание"),(4, "задание")]) ]

def get_topic_list(request):
    topic_list = []
    max_available = Student.objects.get(username=request.user).lecture_pos
    lecture_objs_available = Lecture.objects.values_list('lecture_id', 'lecture_name').filter(position__lte=max_available).order_by('position')
    for lecture_obj in lecture_objs_available:
        lecture_id = lecture_obj[0]
        task_objs = Task.objects.values_list('task_id', 'task_name').filter(lecture=lecture_id)
        topic_list.append((lecture_obj[0], lecture_obj[1], list(task_objs)))

    lecture_objs_lock = Lecture.objects.values_list('lecture_name').filter(position__gt=max_available).order_by('position')
    topic_list_lock = []
    for lecture_obj_lock in list(lecture_objs_lock):
        topic_list_lock.append(lecture_obj_lock[0])
        
    return render(request, 'topic_list.html', {'topic_list': topic_list, 'topic_list_lock': list(topic_list_lock)})

# Отрисовка HTML-шаблона страницы учебника
def get_book(request):
    return render(request, 'book.html')

# Отрисовка HTML-шаблона страницы c заданием
def get_task(request):
    global TASK_ID
    TASK_ID = request.GET.get('id')
    obj = Task.objects.values_list('task_text', 'task_solution', 'task_max_points').filter(task_id=TASK_ID)
    print(obj)
    task = obj[0][0]
    reference_quary = obj[0][1]
    global REFERENCE_RESULT
    global TASK_POINTS
    TASK_POINTS = obj[0][2]
    with fdb.connect(
        database=settings.RDB_CONF['database'], 
        user=settings.RDB_CONF['user'], 
        password=settings.RDB_CONF['password'], 
        charset=settings.RDB_CONF['charset']) as con:
        cur = con.cursor()
        cur.execute(reference_quary)
        REFERENCE_RESULT = cur.fetchall()
        cur.close()
    
    response = {
        "task" : task,
        "number_task": TASK_ID,
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
        charset=settings.RDB_CONF['charset']) as con:
        cur = con.cursor()
        cur.execute(sql_statement)
        result = cur.fetchall()
        cur.close()
    if REFERENCE_RESULT == result:
        equal = True

        id_user = Student.objects.get(username=request.user)
        id_task = Task.objects.get(task_id=TASK_ID)

        p = Points(point=TASK_POINTS,task=id_task,auth_user=id_user,answer=sql_statement)
        p.save()

    else:
        equal = False

    last_available = int(Student.objects.values_list("lecture_pos",  flat=True).filter(username=request.user)[0])
    lecture = int(Task.objects.values_list("lecture", flat=True).filter(task_id=TASK_ID)[0])
    lecture_pos = int(Lecture.objects.values_list("position", flat=True).filter(lecture_id=lecture)[0])
    if last_available == lecture_pos:
        max_points = Task.objects.filter(lecture_id=lecture).aggregate(Sum('task_max_points'))['task_max_points__sum']
        id_user = int(Student.objects.values_list('id', flat=True).filter(username=request.user)[0])
        all_points = Points.objects.values_list("point","task").filter(auth_user=id_user)
        list_tasks = list(Task.objects.values_list("task_id", flat=True).filter(lecture_id=lecture))
        sum_student = 0
        for point, task in list(all_points):
            if task in list_tasks:
                sum_student += point
        
        if sum_student/max_points >= 0.8:
            st = Student.objects.get(id=id_user)
            st.lecture_pos += 1
            st.save()
    
    
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
        charset=settings.RDB_CONF['charset']) as con:
        cur = con.cursor()
        cur.execute(f'select * from {selected_table};')
        result = cur.fetchall()
        cur.close()
    
    response = {
        "result" : result
    }

    return JsonResponse(data=response)

# Отрисовка HTML-шаблона страницы с решениями студентов
def get_solutions(request):
    return render(request, 'solutions.html')