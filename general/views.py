from django.shortcuts import render

# Отрисовка HTML-шаблона страницы входа
def get_signin(request):
    return render(request, 'signin.html')

# Отрисовка HTML-шаблона страницы регистрации
def get_signup(request):
    return render(request, 'signup.html')
