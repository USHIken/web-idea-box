from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, DeleteView
)

from main import utils
from main.models import Content
 

class ContentListView(ListView):
    template_name = "main/index.html"
    model = Content
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ContentDetailView(DetailView):
    template_name = "main/detail.html"
    model = Content
    context_object_name = 'content'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_embed"] = self.object.content_type in utils.EMBED_TYPES
        return context


class ContentDeleteView(DeleteView):
    model = Content
    success_url = reverse_lazy('main:index')

    def post(self, request, *args, **kwargs):
        content_creator = self.get_object().creator
        if content_creator == request.user:
            return self.delete(request, *args, **kwargs)
        else:
            raise PermissionDenied("投稿ユーザー以外は投稿を削除できません。")
