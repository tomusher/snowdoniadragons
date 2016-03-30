from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from jsonfield import JSONField

from wagtail.wagtailcore.models import Page, PageManager
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, PageChooserPanel, TabbedInterface, ObjectList
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from base.models import LinkFields, Game

class SessionManager(PageManager):
    def upcoming(self):
        return self.get_queryset().filter(date__gte=datetime.now())

    def past(self):
        return self.get_queryset().filter(date__lt=datetime.now())

class SessionIndex(Page):
    subpage_types = ['Session',]

class Session(Page, ClusterableModel):
    name = models.CharField(max_length=255, blank=True, help_text="Leave blank if this is just a regular session")
    date = models.DateTimeField("Session date")
    summary = models.CharField(max_length=500, blank=True)
    venue = models.ForeignKey('base.Venue', null=True, blank=True, help_text="Only needed if the venue is different from the regular venue")
    forum_thread = models.URLField(blank=True)

    objects = SessionManager()
    parent_page_types = ['group.Group',]

    content_panels = [
        FieldPanel('date', classname="title"),
        FieldPanel('forum_thread'),
        FieldPanel('summary'),
        FieldPanel('venue'),

        InlinePanel('games_played', label='Games Played'),
        InlinePanel('related_media', label='Related'),
        InlinePanel('images', label='Images'),
    ]

    related_panels = [
        InlinePanel('games_played', label='Games Played'),
        InlinePanel('related_media', label='Related'),
        InlinePanel('images', label='Images'),
    ]

    def clean(self):
        super().clean()
        self.title = 'Session '+self.date.strftime("%Y-%m-%d")

class SessionRelated(LinkFields):
    page = ParentalKey('Session', related_name='related_media')
    title = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        FieldPanel('title')
    ]

class SessionImage(models.Model):
    page = ParentalKey('Session', related_name='images')
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    caption = models.CharField(max_length=255, blank=True)
    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption')
    ]

class SessionGame(models.Model):
    page = ParentalKey('Session', related_name='games_played')
    game = models.ForeignKey('base.Game')
    times_played = models.IntegerField()

    panels = [
        FieldRowPanel([
            FieldPanel('game', classname="col12 boardgame-selectize"),
            FieldPanel('times_played'),
        ])
    ]
