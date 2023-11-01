from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django import forms
from django.contrib.auth.models import User


class MyAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 
                                                           'placeholder': 'Логин',
                                                           'class': 'input-login'}))
    password = forms.CharField(
        label= None,
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'placeholder': 'Пароль',
                                          'class': 'input-password'}),
    )


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True,
                                                               'placeholder': 'Имя',
                                                               'class': 'input-fio'}))
    
    last_name = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True,
                                                               'placeholder': 'Фамилия',
                                                               'class': 'input-fio'}))
    
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 
                                                           'placeholder': 'Логин',
                                                           'class': 'input-login'}))
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True, 
                                                           'placeholder': 'Email',
                                                           'class': 'input-email'}))

    password1 = forms.CharField(
        label= None,
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'placeholder': 'Пароль',
                                          'class': 'input-password'}),
    
    )

    password2 = forms.CharField(
        label= None,
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'placeholder': 'Повторите пароль',
                                          'class': 'input-password'}),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', )