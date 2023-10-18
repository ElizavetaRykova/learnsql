from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms


class MyForm(AuthenticationForm):
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
