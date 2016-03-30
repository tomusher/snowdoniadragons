from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from wagtail.wagtailcore.models import Page

from base.models import LinkIndex
from group.models import Group
from session.models import Session
from blog.models import BlogArticle

class HomePage(Page):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update({
            'groups': Group.objects.descendant_of(self),
            'upcoming_sessions': Session.objects.upcoming().live().descendant_of(self),
            'recent_sessions': Session.objects.past().live().descendant_of(self)[:10],
            'blog_posts': BlogArticle.objects.live().descendant_of(self)[:10],
            'links': LinkIndex.objects.live().descendant_of(self)
        })
        return context
