from __future__ import unicode_literals
import requests
import io

from django.core.files.base import ContentFile
from django.db import models
from django.template.loader import render_to_string

from jsonfield import JSONField
from boardgamegeek import BoardGameGeek

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel

class Game(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='games/', null=True, blank=True)
    bgg_id = models.CharField(max_length=50)
    data = JSONField(default={})

    def save(self, *args, **kwargs):
        bgg = BoardGameGeek()
        game = bgg.game(game_id=self.bgg_id)
        self.name = "{0} ({1})".format(game.name, game.year)
        if game.image:
            img_response  = requests.get(game.image)
            filename = game.image.split('/')[-1]
            self.image.save(filename, ContentFile(img_response.content), save=False)
        self.data['url'] = "https://boardgamegeek.com/boardgame/{0}".format(game.id)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('bgg_id'),
    ]

class Venue(models.Model):
    name = models.CharField(max_length=255)
    coords = models.CharField(max_length=255)
    description = RichTextField()

    def __str__(self):
        return self.name

class LinkIndex(Page):
    subpage_types = ['Link',]

class Link(Page):
    description = models.TextField()
    image = models.ForeignKey('wagtailimages.Image')
    link_url = models.URLField()

    content_panels = [
        FieldPanel('title', classname="title"),
        FieldPanel('description'),
        FieldPanel('link_url'),
        ImageChooserPanel('image')
    ]

    parent_page_types = ['LinkIndex',]

class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page')
    ]

    class Meta:
        abstract = True

