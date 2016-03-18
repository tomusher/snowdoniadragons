from django.utils.html import format_html, format_html_join
from django.conf import settings

from wagtail.wagtailcore import hooks
from wagtailmodeladmin.options import ModelAdmin, wagtailmodeladmin_register

from base.models import Game, Link
from session.models import Session
from group.models import Group
from blog.models import BlogArticle

class SessionModelAdmin(ModelAdmin):
    model = Session
    menu_label = 'Sessions'
    list_display = ('game_group', 'date',)
    search_fields = ('date', 'game_group')

class GroupModelAdmin(ModelAdmin):
    model = Group
    menu_label = 'Group'
    list_display = ('name',)
    search_fields = {'name',}

class GameModelAdmin(ModelAdmin):
    model = Game
    menu_label = 'Game'
    list_display = ('name',)
    search_fields = {'name',}

class LinkModelAdmin(ModelAdmin):
    model = Link
    menu_label = 'Link'
    list_display = ('name',)
    search_fields = {'name',}

wagtailmodeladmin_register(SessionModelAdmin)
wagtailmodeladmin_register(GroupModelAdmin)
wagtailmodeladmin_register(GameModelAdmin)
wagtailmodeladmin_register(LinkModelAdmin)

@hooks.register('insert_editor_js')
def selectize_js():
    js_files = [
        'js/admin/selectize.js',
        'js/admin/admin.js'
    ]

    js_includes = format_html_join('\n', '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )

    return js_includes + format_html(
        """
        <script>
           registerHalloPlugin('hallohtml');
        </script>
        """
    )

@hooks.register('insert_editor_css')
def selectize_css():
    css_files = [
        'css/admin/admin.css',
        'css/admin/selectize.css',
        'css/admin/selectize.bootstrap3.css'
    ]

    css_includes = format_html_join('\n', '<link rel="stylesheet" href="{0}{1}">',
        ((settings.STATIC_URL, filename) for filename in css_files)
    )

    return css_includes
