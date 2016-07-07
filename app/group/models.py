from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.template.response import TemplateResponse

from wagtail.wagtailcore.models import Page, PageManager
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, PageChooserPanel, TabbedInterface, ObjectList, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailcore.fields import RichTextField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.wagtailcore.blocks import StructBlock, StreamBlock, PageChooserBlock, URLBlock
from wagtail.utils.pagination import paginate

from base.models import LinkFields, Game
from .blocks import GameBlock
from .forms import SessionForm

class SessionManager(PageManager):
    def upcoming(self):
        return self.get_queryset().filter(date__gte=datetime.now())

    def past(self):
        return self.get_queryset().filter(date__lt=datetime.now())

class Session(RoutablePageMixin, Page):
    name = models.CharField(max_length=255, blank=True, help_text="Leave blank if this is just a regular session")
    date = models.DateTimeField("Session date")
    summary = models.CharField(max_length=500, blank=True)
    venue = models.ForeignKey('base.Venue', null=True, blank=True, help_text="Only needed if the venue is different from the regular venue")
    forum_thread = models.URLField(blank=True)

    related = StreamField([
        ('blog', PageChooserBlock()),
        ('url', URLBlock())
    ], null=True, blank=True)

    objects = SessionManager()
    parent_page_types = ['group.Group',]

    content_panels = [
        FieldPanel('date', classname="title"),
        FieldPanel('forum_thread'),
        FieldPanel('summary'),
        FieldPanel('venue'),

        InlinePanel('games_played', label='Games Played'),
        InlinePanel('images', label='Images'),
        InlinePanel('related_media', label='Related'),
    ]

    base_form_class = SessionForm

    def clean(self):
        super().clean()
        self.title = 'Session '+self.date.strftime("%Y-%m-%d")

class SessionRelated(LinkFields):
    session = ParentalKey('Session', related_name='related_media')
    title = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        FieldPanel('title')
    ]

class SessionImage(models.Model):
    session = ParentalKey('Session', related_name='images')
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
    session = ParentalKey('Session', related_name='games_played')
    game = models.ForeignKey('base.Game')
    times_played = models.PositiveIntegerField(default=1)

    panels = [
        FieldPanel('game', classname="boardgame-selectize"),
        FieldPanel('times_played'),
    ]

class GroupIndex(Page):
    subpage_types = ['group.Group',]

class Group(RoutablePageMixin, Page):
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

    subpage_types = ['group.Session',]
    parent_page_types = ['group.GroupIndex',]

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
        return SessionImage.objects.filter(session__in=sessions)

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

    @route(r'^sessions/$')
    def sessions(self, request):
        context = self.get_context(request)
        paginator, context['sessions'] = paginate(request, self.past_sessions, per_page=20)
        return TemplateResponse(
            request,
            'group/sessions.html',
            context
        )

