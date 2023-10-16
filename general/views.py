from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

# Форма входа
def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# Отрисовка HTML-шаблона страницы регистрации
def get_signup(request):
    return render(request, 'signup.html')

# Отрисовка HTML-шаблона страницы со списком тем
def get_topic_list(request):
    return render(request, 'topic_list.html')