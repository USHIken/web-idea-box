from django.shortcuts import render
from django.http import HttpResponse


# from .models import Content
from django.views.generic import ListView, TemplateView
 
 
class ContentList(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "Tatsuya"
        return context