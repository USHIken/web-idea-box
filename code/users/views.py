from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import LoginForm, SignUpForm


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
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())