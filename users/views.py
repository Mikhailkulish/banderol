import logging

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserUpdateForm, UserLoginForm
from users.models import User

logger = logging.getLogger(__name__)


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать в Ban de Rol'
        message = 'Спасибо, что зарегистрировались в Ban de Rol!'
        recipient_list = [user_email]

        try:
            send_mail(subject, message, None, recipient_list)
        except Exception:
            logger.exception(
                "Не удалось отправить приветственное письмо на %s", user_email
            )


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = UserLoginForm
    redirect_authenticated_user = True


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('main:main')

    def get_object(self, queryset=None):
        return self.request.user
