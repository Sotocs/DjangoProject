from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserRegistrationForm, CustomLoginForm, ProfileEditForm
from .models import CustomUser


def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # создаёт пользователя
            # Отправляем приветственное письмо
            send_mail(
                subject='Добро пожаловать!',
                message=f'Привет, {user.email}! Спасибо за регистрацию в нашем сервисе.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            login(request, user)  # сразу авторизуем
            return redirect('catalog:home')  # или любой другой URL после регистрации
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'register.html', {'form': form})


class LoginView(FormView):
    form_class = CustomLoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileEditForm
    template_name = 'profile_edit.html'
    success_url = reverse_lazy('catalog:home')  # или на страницу профиля /dashboard и т.п.

    def get_object(self, queryset=None):
        # Разрешаем редактировать только свой профиль
        return self.request.user