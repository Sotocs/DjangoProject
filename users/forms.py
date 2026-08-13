from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        # username не нужен, так как он None в модели
        if commit:
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    # Переопределяем username на email
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))