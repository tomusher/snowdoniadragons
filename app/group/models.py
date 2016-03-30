from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.template.response import TemplateResponse

from wagtail.wagtailcore.models import Page
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailcore.fields import RichTextField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from session.models import SessionImage, Session

class GroupIndex(Page):
    pass

class Group(RoutablePageMixin, Page, ClusterableModel):
    summary = models.CharField(max_length=500)
    description = RichTextField()
    venue = models.ForeignKey('base.venue', null=True, blank=True)
    colour = models.CharField(max_length=8)
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    forum_url = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)

    content_panels = [
        FieldPanel('title'),
        FieldPanel('summary'),
        FieldPanel('venue'),
        FieldPanel('description'),
        FieldPanel('colour'),
        ImageChooserPanel('main_image')
    ]

    promote_panels = Page.promote_panels + [
        MultiFieldPanel([
            FieldPanel('forum_url'),
            FieldPanel('contact_email')
        ], heading="Find out More")
    ]

    subpage_types = ['session.Session',]

    def __str__(self):
        return self.title

    @property
    def past_sessions(self):
        return Session.objects.descendant_of(self).filter(date__lte=datetime.now())

    @property
    def next_session(self):
        session = Session.objects.descendant_of(self).filter(date__gte=datetime.now()).first()
        return session

    @property
    def next_venue(self):
        if self.next_session and self.next_session.venue:
            return self.next_session.venue
        else:
            return self.venue

    @property
    def all_images(self):
        sessions = self.past_sessions
        return SessionImage.objects.filter(page__in=sessions)

    @route(r'^$')
    def base(self, request):
        return TemplateResponse(
            request,
            self.get_template(request),
            self.get_context(request)
        )

    @route(r'^gallery/$')
    def gallery(self, request):
        return TemplateResponse(
            request,
            'group/gallery.html',
            self.get_context(request)
        )
