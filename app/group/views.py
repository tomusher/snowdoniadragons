from django.shortcuts import render

from django.views.generic import DetailView

from .models import Group

class GroupDetailView(DetailView):
    model = Group
    template_name = "group.html"
