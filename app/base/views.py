from datetime import datetime

from django.shortcuts import render
from django.views.generic import TemplateView

from group.models import Group
from session.models import Session

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(*args, **kwargs):
        return {
            'groups': Group.objects.all(),
            'upcoming_sessions': Session.objects.filter(date__gte=datetime.now()),
            'recent_sessions': Session.objects.filter(date__lt=datetime.now())[:10]
        }
