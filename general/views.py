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
import subprocess
import time
import os

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
                return redirect('/topic_list')
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
            return redirect('/topic_list')
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

    with fdb.connect_server(server='localhost', user=settings.RDB_CONF['user'], password=settings.RDB_CONF['password']) as srv:
        home_directory = srv.info.home_directory

    subprocess.run([f"{home_directory}nbackup.exe", "-L", f"{home_directory}examples/empbuild/employee.fdb", "-u", settings.RDB_CONF['user'], "-p", settings.RDB_CONF['password']])
    time.sleep(1)

    with fdb.connect(
        database=settings.RDB_CONF['database'], 
        user=settings.RDB_CONF['user'], 
        password=settings.RDB_CONF['password'], 
        charset=settings.RDB_CONF['charset']) as con:
        cur = con.cursor()
        cur.execute(reference_quary)
        REFERENCE_RESULT = cur.fetchall()
        cur.close()
    
    delta_file = home_directory + "examples/empbuild/employee.fdb.delta"
    if os.path.exists(delta_file): 
        os.remove(delta_file)
    subprocess.run([f"{home_directory}nbackup.exe", "-F", f"{home_directory}examples/empbuild/employee.fdb"])

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

    with fdb.connect_server(server='localhost', user=settings.RDB_CONF['user'], password=settings.RDB_CONF['password']) as srv:
        home_directory = srv.info.home_directory
    subprocess.run([f"{home_directory}nbackup.exe", "-L", f"{home_directory}examples/empbuild/employee.fdb", "-u", settings.RDB_CONF['user'], "-p", settings.RDB_CONF['password']])
    time.sleep(1)

    with fdb.connect(
        database=settings.RDB_CONF_STUDENT['database'], 
        user=settings.RDB_CONF_STUDENT['user'], 
        password=settings.RDB_CONF_STUDENT['password'], 
        charset=settings.RDB_CONF_STUDENT['charset']) as con:
        cur = con.cursor()
        cur.execute(sql_statement)
        result = cur.fetchall()
        cur.close()
    if REFERENCE_RESULT == result:
        equal = True

        id_user = Student.objects.get(username=request.user)
        id_task = Task.objects.get(task_id=TASK_ID)

        p = Points.objects.values_list('point_id').filter(task=id_task,auth_user=id_user)
        if not p:
            pt = Points(point=TASK_POINTS,task=id_task,auth_user=id_user,answer=sql_statement)
            pt.save()

    else:
        equal = False

    delta_file = home_directory + "examples/empbuild/employee.fdb.delta"
    if os.path.exists(delta_file): 
        os.remove(delta_file)
    subprocess.run([f"{home_directory}nbackup.exe", "-F", f"{home_directory}examples/empbuild/employee.fdb"])


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
    solutions = []
    questions = []
    answers = []
    comments = []
    if request.user.is_staff == True:
        objs = Points.objects.values_list('point_id', 'answer', 'auth_user_id', 'task_id', 'is_viewed').filter(is_viewed=False)
        for obj in objs:
            solution = []
            solution.append(obj[0])
            solution.append(obj[1])
            name = Student.objects.values_list('first_name', 'last_name').filter(id=obj[2])
            solution.append(f"{name[0][0]} {name[0][1]}")
            task_name = Task.objects.values_list('task_name', 'task_text').filter(task_id=obj[3])
            solution.append(f"{task_name[0][0]}")
            solution.append(f"{task_name[0][1]}")
            solutions.append(solution)
        
        objs = Question.objects.values_list('question_id', 'question', 'auth_user_id', 'task_id').filter(is_viewed=False)
        for obj in objs:
            question = []
            question.append(obj[0])
            question.append(obj[1])
            name = Student.objects.values_list('first_name', 'last_name').filter(id=obj[2])
            question.append(f"{name[0][0]} {name[0][1]}")
            task_name = Task.objects.values_list('task_name', 'task_text').filter(task_id=obj[3])
            question.append(f"{task_name[0][0]}")
            question.append(f"{task_name[0][1]}")
            questions.append(question)

    else:
        id_user = Student.objects.get(username=request.user).id
        objs = Question.objects.values_list('question_id', 'question', 'comment', 'task_id', 'auth_user_id').filter(auth_user=id_user, is_viewed_student=False)
        for obj in objs:
            answer = []
            answer.append(obj[0])
            answer.append(obj[1])
            answer.append(obj[2])
            task_name = Task.objects.values_list('task_name').filter(task_id=obj[3])
            answer.append(f"{task_name[0][0]}")
            answers.append(answer)
        
        objs = Points.objects.values_list('point_id', 'answer', 'task_id', 'comment').filter(auth_user=id_user, is_viewed=False)
        for obj in objs:
            comment = []
            comment.append(obj[0])
            comment.append(obj[1])
            task_name = Task.objects.values_list('task_name').filter(task_id=obj[2])
            comment.append(f"{task_name[0][0]}")
            comment.append(obj[3])
            comments.append(comment)


    respons = {
        "solutions": solutions,
        "questions": questions,
        "answers": answers,
        "comments": comments

    }
    return render(request, 'solutions.html', respons)

def add_comment(request):
    text_comment = request.POST.get('text_comment')
    point_id = request.POST.get('point_id')

    point = Points.objects.get(point_id=point_id)
    point.comment = text_comment
    point.is_viewed = True
    point.save()

    response = {
        "added": True
    }
    return JsonResponse(data=response)

def add_answer(request):
    text_answer = request.POST.get('text_answer')
    question_id = request.POST.get('question_id')

    question = Question.objects.get(question_id=question_id)
    question.comment = text_answer
    question.is_viewed = True
    question.save()

    response = {
        "added": True
    }
    return JsonResponse(data=response)

def add_question(request):
    text_question = request.POST.get('text_question')
    id_user = Student.objects.get(username=request.user)
    id_task = Task.objects.get(task_id=TASK_ID)
    question = Question(question=text_question,task=id_task,auth_user=id_user)
    question.save()

    response = {
        "added": True
    }
    return JsonResponse(data=response)

def view_answer(request):
    question_id = request.POST.get('question_id')
    question = Question.objects.get(question_id=question_id)
    question.is_viewed_student = True
    question.save()

    response = {
        "added": True
    }
    return JsonResponse(data=response)

def view_comment(request):
    point_id = request.POST.get('point_id')
    point = Points.objects.get(point_id=point_id)
    point.is_viewed = True
    point.save()

    response = {
        "added": True
    }
    return JsonResponse(data=response)