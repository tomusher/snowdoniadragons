from __future__ import unicode_literals

from django.db import models
from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from jsonfield import JSONField

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, PageChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from base.models import LinkFields, Game

class SessionIndex(Page):
    pass

class Session(ClusterableModel):
    game_group = models.ForeignKey('group.Group', null=True, blank=True)
    name = models.CharField(max_length=255, blank=True, help_text="Leave blank if this is just a regular session")
    date = models.DateField("Session date")
    summary = models.CharField(max_length=500, blank=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('date'),
            FieldPanel('game_group'),
            FieldPanel('summary'),
        ]),
        InlinePanel('games_played', label='Games Played'),
        InlinePanel('related_media', label='Related'),
        InlinePanel('images', label='Images'),
    ]

    parent_page_types = ['SessionIndex']

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
            FieldPanel('game', classname="col7 boardgame-selectize"),
            FieldPanel('times_played', classname="col5"),
        ])
    ]
