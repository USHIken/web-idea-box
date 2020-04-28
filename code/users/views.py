from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from main.models import Content
from users.models import User
from users.forms import LoginForm, SignUpForm


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
