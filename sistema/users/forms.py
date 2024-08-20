from django import forms
from .models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
            'autofocus': True
        }),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }),
        label='Password'
    )

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'user_type', 'password']
        labels = {
            'first_name': 'Nome de Usuário',
            'email': 'Email',
            'user_type': 'Tipo de Usuário',
            'password': 'Senha',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de Usuário', }),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', }),
            'user_type': forms.Select(attrs={'class': 'form-control', }),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha', }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['first_name'].replace(' ', '_').lower()
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user