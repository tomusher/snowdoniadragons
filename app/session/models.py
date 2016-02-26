from __future__ import unicode_literals

from django.db import models
from django import forms

from jsonfield import JSONField

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from base.models import LinkFields

class SessionIndex(Page):
    pass

class Session(ClusterableModel):
    date = models.DateField("Session date")
    summary = models.CharField(max_length=500)
    game_group = models.ForeignKey('group.Group', null=True, blank=True)
    played_games = JSONField(null=True, blank=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('game_group'),
            FieldPanel('summary'),
            FieldPanel('played_games', classname="boardgame-selectize", widget=forms.TextInput)
        ]),
        InlinePanel('related_media', label='Related'),
        InlinePanel('images', label='Images'),
    ]

    parent_page_types = ['SessionIndex']

class SessionRelated(LinkFields):
    page = ParentalKey('Session', related_name='related_media')

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


class SessionGamePlayed(models.Model):
    game = models.CharField(max_length=255)
    page = ParentalKey('Session', related_name='games_played')
