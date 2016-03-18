from django.shortcuts import render

from django.views.generic import DetailView

from .models import BlogArtice

class BlogDetailView(DetailView):
    model = BlogArticle
    template_name = "blogarticle.html"
