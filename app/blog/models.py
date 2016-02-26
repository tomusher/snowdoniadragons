from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.wagtailsearch import index
from modelcluster.models import ClusterableModel

class BlogIndex(Page):
    pass

class BlogArticle(ClusterableModel):
    title = models.CharField(max_length=255)
    date = models.DateField("Post date")
    intro = models.CharField(max_length=255)
    body = RichTextField(blank=True)

    content_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname="title"),
            FieldPanel('date'),
            FieldPanel('intro'),
            FieldPanel('body', classname='full')
        ])
    ]

    parent_page_types = ['BlogIndex']
