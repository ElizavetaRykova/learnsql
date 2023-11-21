from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# from django.contrib.auth.forms import AuthenticationForm
from .forms import MyAuthenticationForm, RegisterForm

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
            return redirect('lectures/')
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form': form})

# Отрисовка HTML-шаблона страницы со списком тем
def get_lectures(request):
    return render(request, 'lectures.html')

# Отрисовка HTML-шаблона страницы учебника
def get_book(request):
    return render(request, 'book.html')