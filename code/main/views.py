from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView

from main.models import Content
 

class ContentListView(ListView):
    template_name = "main/index.html"
    model = Content
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "Tatsuya"
        return context


class ContentDetailView(DetailView):
    pass
