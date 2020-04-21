from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, DeleteView,
    CreateView, UpdateView,
)

from main import utils
from main.forms import ContentCreateForm, ContentUpdateForm
from main.models import Content


class ContentListView(ListView):
    template_name = "main/index.html"
    model = Content
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ContentCreateView(LoginRequiredMixin, CreateView):
    template_name = "main/create_and_update.html"
    model = Content
    form_class = ContentCreateForm
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'main:detail', kwargs={'pk': self.object.pk})


class ContentDetailView(DetailView):
    template_name = "main/detail.html"
    model = Content
    context_object_name = 'content'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_embed"] = self.object.content_type in utils.EMBED_TYPES
        context["is_creator"] = self.object.creator == self.request.user
        return context


class ContentUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "main/create_and_update.html"
    model = Content
    form_class = ContentUpdateForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'main:detail', kwargs={'pk': self.object.pk})

    def get(self, request, *args, **kwargs):
        content_creator = self.get_object().creator
        if content_creator == request.user:
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied("投稿ユーザー以外は投稿を削除できません。")


class ContentDeleteView(LoginRequiredMixin, DeleteView):
    model = Content
    success_url = reverse_lazy('main:index')

    def post(self, request, *args, **kwargs):
        content_creator = self.get_object().creator
        if content_creator == request.user:
            return self.delete(request, *args, **kwargs)
        else:
            raise PermissionDenied("投稿ユーザー以外は投稿を削除できません。")
