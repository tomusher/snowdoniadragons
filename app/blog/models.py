from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsearch import index
from modelcluster.models import ClusterableModel
from wagtail.utils.pagination import paginate

class BlogIndex(Page):
    subpage_types = ['BlogArticle',]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        articles = BlogArticle.objects.live().descendant_of(self).order_by('-date')
        paginator, context['blog_articles'] = paginate(request, articles, per_page=18)
        return context

class BlogArticle(Page):
    date = models.DateField("Post date")
    author = models.CharField(max_length=255)
    intro = models.CharField(max_length=255)
    body = RichTextField(blank=True)
    body_stream = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])
    related_group = models.ForeignKey(
        'group.Group',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    parent_page_types = ['BlogIndex',]

    content_panels = [
        FieldPanel('title', classname="title"),
        FieldPanel('date'),
        FieldPanel('author'),
        FieldPanel('related_group'),
        ImageChooserPanel('main_image'),
        FieldPanel('intro'),
        StreamFieldPanel('body_stream')
    ]
