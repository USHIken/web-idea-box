from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, DeleteView,
    CreateView, UpdateView,
)

from main.forms import ContentCreateForm, ContentUpdateForm
from main.models import Content
from main.utils import CONTENT_TYPES


class ContentListView(ListView):
    template_name = "main/index.html"
    model = Content
    paginate_by = 20

    def get_context_data(self):
        context = super().get_context_data()
        content_list_by_type = {}
        for content_type, _ in CONTENT_TYPES:
            queryset = self.model.objects.filter(content_type=content_type)
            content_list_by_type[content_type] = queryset[:6]
        context["content_list_by_type"] = content_list_by_type
        context["recent_contents"] = self.model.objects.all()[:6]
        return context


class ContentListByTypeView(ListView):
    template_name = "main/content_list_by_type.html"
    model = Content
    paginate_by = 3

    def get_queryset(self, content_type):
        queryset = self.model.objects.filter(content_type=content_type)
        queryset = queryset.order_by('-created_at')
        return queryset

    def get(self, request, content_type, *args, **kwargs):
        self.object_list = self.get_queryset(content_type)
        context = self.get_context_data()
        context["content_type"] = content_type
        return self.render_to_response(context)


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
        context["is_creator"] = self.object.is_created_by(self.request.user)
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
        content = self.get_object()
        if content.is_created_by(request.user):
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied("投稿ユーザー以外は投稿を編集できません。")


class ContentDeleteView(LoginRequiredMixin, DeleteView):
    model = Content
    success_url = reverse_lazy('main:index')

    def post(self, request, *args, **kwargs):
        content_creator = self.get_object().creator
        if content_creator == request.user:
            return self.delete(request, *args, **kwargs)
        else:
            raise PermissionDenied("投稿ユーザー以外は投稿を削除できません。")

def mentor(request):
    return render(request, 'main/mentor.html')