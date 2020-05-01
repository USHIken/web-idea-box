from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from main.models import Content
from users.models import User
from users.forms import (
    LoginForm, SignUpForm, ProfileUpdateForm,
    UserPasswordChangeForm,
)


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'users/login_and_registration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["host"] = self.request.get_host()
        print(self.request.get_host())
        return context

    def post(self, request, *args, **kwargs):
        print(request.POST)
        return super().post(request, *args, **kwargs)


class Logout(LogoutView):
    """ログアウトページ"""
    pass


class Signup(CreateView):
    """登録ページ"""
    form_class = SignUpForm
    template_name = 'users/login_and_registration.html'
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())


class ProfileView(ListView):
    template_name = "users/profile.html"
    model = Content
    paginate_by = 3

    def get_queryset(self, pk):
        queryset = self.model.objects.filter(creator__pk=pk)
        queryset = queryset.order_by('-created_at')
        return queryset

    def get_context_data(self, pk, *args, object_list=None, **kwargs):
        context = super().get_context_data(
            *args, object_list=object_list, **kwargs)
        try:
            context["creator"] = User.objects.get(pk=pk)
        except User.DoesNotExist:
            context["creator"] = None
        return context

    def get(self, request, pk, *args, **kwargs):
        self.object_list = self.get_queryset(pk)
        context = self.get_context_data(pk)
        if context["creator"] is None:
            return render(request, '404.html', context, status=404)
        else:
            return self.render_to_response(context)


class ProfileUpdateView(UpdateView):
    template_name = "users/update.html"
    model = User
    form_class = ProfileUpdateForm

    def get_success_url(self):
        return reverse_lazy(
            "users:profile", kwargs={'pk': self.request.user.pk})

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)


class UserPasswordChangeView(PasswordChangeView):
    template_name = "users/password_change.html"
    form_class = UserPasswordChangeForm

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy('users:profile', kwargs={'pk': user.pk})
