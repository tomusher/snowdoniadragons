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

