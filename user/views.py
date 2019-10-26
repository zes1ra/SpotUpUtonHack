from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, UserUpdateForm
# from cart.views import CountInCart
from .models import UserCustom
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)


class UserCreate(CreateView):
    model = UserCustom
    form_class = UserRegistrationForm
    template_name = 'user/user_registration.html'

    def get_success_url(self):
        self.object.set_password(self.object.password)
        self.object.save()
        return reverse_lazy('login')


class UserDetail(DetailView):
    model = UserCustom
    template_name = 'user/user_detail.html'

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = UserCustom
    form_class = UserUpdateForm
    template_name = 'user/user_update.html'  # 'form/update_form.html'

    def get_object(self, queryset=None):
        # if UserCustom.is_superuser:
        #     return self.request.user
        return self.request.user.custom

    def get_success_url(self):
        return reverse_lazy('user-detail')


class UserLoginView(LoginView):
    template_name = 'registration/login.html'


class UserLogoutView(LogoutView):
    template_name = 'registration/logged_out.html'


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change.html'


class UserPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'


class UserPasswordResetView(LoginRequiredMixin, PasswordResetView):
    template_name = 'registration/password_reset.html'


class UserPasswordResetDoneView(LoginRequiredMixin, PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class UserPasswordResetConfirmView(LoginRequiredMixin, PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'


class UserPasswordResetCompleteView(LoginRequiredMixin, PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
