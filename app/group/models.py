from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

class GroupIndex(Page):
    pass

class Group(ClusterableModel):
    name = models.CharField(max_length=255)
    summary = models.CharField(max_length=500)
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('name', classname="title"),
            FieldPanel('summary'),
            ImageChooserPanel('main_image')
        ])
    ]

    parent_page_types = ['GroupIndex']

    def __str__(self):
        return self.name
