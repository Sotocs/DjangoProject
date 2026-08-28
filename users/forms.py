from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser


class CustomUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = CustomUser
        fields = ["email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        # username не нужен, так как он None в модели
        if commit:
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    # Переопределяем username на email
    username = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email", "phone_number", "country", "avatar"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email адрес",
                    "readonly": True,  # опционально: запретить менять email в профиле
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Номер телефона",
                }
            ),
            "country": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Страна",
                }
            ),
            "avatar": forms.FileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если хочешь разрешить менять email — убери строку ниже.
        # Но помни: email уникальный, и при смене нужно проверять, не занят ли он.
        self.fields["email"].required = True
        self.fields["email"].widget.attrs["readonly"] = True
