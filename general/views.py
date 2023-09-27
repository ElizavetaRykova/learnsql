from django.shortcuts import render

# Отрисовка HTML-шаблона страницы регистрации
def get_signin(request):
    return render(request, 'signin.html')
