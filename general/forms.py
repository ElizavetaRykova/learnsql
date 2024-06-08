from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm, PasswordChangeForm, PasswordResetForm
from django import forms
from django.contrib.auth.models import User
from general.models import Student
from django.utils.translation import gettext, gettext_lazy as _

class MyAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label=_(""),
        widget=forms.TextInput(attrs={'autofocus': True, 
                                                           'placeholder': 'Логин',
                                                           'class': 'input-login'}))
    password = forms.CharField(
        label=_(""),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'placeholder': 'Пароль',
                                          'class': 'input-password'}),
    )


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_(""),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'placeholder': 'Старый пароль', 'autofocus': True, 'class': 'input-password'}),
    )
    new_password1 = forms.CharField(
        label=_(""),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'placeholder': 'Пароль',
                                          'class': 'input-password'}),
    )
    new_password2 = forms.CharField(
        label=_(""),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'placeholder': 'Повторите пароль',
                                          'class': 'input-password'}),
    )


class ForgotPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        label=_(""),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
                                       'placeholder': 'Email',
                                       'class': 'input-email'}),
    )


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label=_(""),
        widget=forms.TextInput(attrs={'autofocus': True,
                                      'placeholder': 'Имя',
                                      'class': 'input-fio'}))
    
    last_name = forms.CharField(
        label=_(""),
        widget=forms.TextInput(attrs={'autofocus': True,
                                      'placeholder': 'Фамилия',
                                      'class': 'input-fio'}))
    
    username = UsernameField(
        label=_(""),
        widget=forms.TextInput(attrs={'autofocus': True, 
                                      'placeholder': 'Логин',
                                      'class': 'input-login'}))
    
    email = forms.EmailField(
        label=_(""),
        widget=forms.EmailInput(attrs={'autofocus': True, 
                                'placeholder': 'Email',
                                'class': 'input-email'}))

    password1 = forms.CharField(
        label=_(""),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'placeholder': 'Пароль',
                                          'class': 'input-password'}),
    
    )

    password2 = forms.CharField(
        label=_(""),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'placeholder': 'Повторите пароль',
                                          'class': 'input-password'}),
    )

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', )



class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select a file', widget=forms.ClearableFileInput(attrs={'accept': '.rst,.png'}))

class EditFileForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}), label='Edit file content')

class FileSelectionForm(forms.Form):
    filename = forms.ChoiceField(choices=[], label='Select a file')
    
    def __init__(self, *args, **kwargs):
        file_choices = kwargs.pop('file_choices', [])
        super().__init__(*args, **kwargs)
        self.fields['filename'].choices = file_choices 