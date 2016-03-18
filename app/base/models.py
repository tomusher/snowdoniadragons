from __future__ import unicode_literals
import requests
import io

from django.core.files.base import ContentFile
from django.db import models
from django.template.loader import render_to_string

from jsonfield import JSONField
from boardgamegeek import BoardGameGeek

from wagtail.wagtailadmin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel

class Game(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='games/', null=True, blank=True)
    bgg_id = models.CharField(max_length=50)
    data = JSONField()

    def save(self, *args, **kwargs):
        bgg = BoardGameGeek()
        game = bgg.game(game_id=self.bgg_id)
        self.name = game.name
        img_response  = requests.get(game.image)
        filename = game.image.split('/')[-1]
        self.image.save(filename, ContentFile(img_response.content), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('bgg_id'),
        FieldPanel('image')
    ]

class Link(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ForeignKey('wagtailimages.Image')

    panels = [
        FieldPanel('name'),
        FieldPanel('description'),
        ImageChooserPanel('image')
    ]

    def __str__(self):
        return self.name

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
