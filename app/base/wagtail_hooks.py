from django.utils.html import format_html, format_html_join
from django.conf import settings

from wagtail.wagtailcore import hooks
from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from wagtail.contrib.modeladmin.helpers import ButtonHelper

from base.models import Game, Venue
from group.models import Group, Session
from blog.models import BlogArticle

from .image_operations import PadOperation

class GroupButtonHelper(ButtonHelper):
    def get_buttons_for_obj(self, obj, *args, **kwargs):
        btns = super().get_buttons_for_obj(obj, *args, **kwargs)
        btns.append(
            {
                'url': '/admin/pages/add/group/session/{0}/'.format(obj.pk),
                'label': 'Add Session',
                'classname': 'button button-small button-secondary',
                'title': 'Add Session'
            }
        )
        btns.append(
            {
                'url': '/admin/pages/{0}/'.format(obj.pk),
                'label': 'View Sessions',
                'classname': 'button button-small button-secondary',
                'title': 'View Sessions'
            }
        )
        return btns

class GameModelAdmin(ModelAdmin):
    model = Game
    menu_label = 'Game'
    list_display = ('name',)
    search_fields = {'name',}

class VenueModelAdmin(ModelAdmin):
    model = Venue
    menu_label = 'Venue'
    list_display = ('name',)
    search_fields = {'name',}

class GroupModelAdmin(ModelAdmin):
    model = Group
    menu_label = 'Group'
    list_display = ('title',)
    search_display = ('title',)

    button_helper_class = GroupButtonHelper

class SessionModelAdmin(ModelAdmin):
    model = Session
    menu_label = 'Session'
    list_display = ('title', 'date')
    search_display = ('title', 'date')

class GameGroupModelAdminGroup(ModelAdminGroup):
    menu_label = 'Groups'
    menu_icon = 'folder-open-inverse'
    items = (GroupModelAdmin, SessionModelAdmin, VenueModelAdmin)

class BlogArticleModelAdmin(ModelAdmin):
    model = BlogArticle
    menu_label = 'Blog Post'
    list_display = ('title', 'date')
    search_display = ('title', 'date')

modeladmin_register(GameModelAdmin)
modeladmin_register(GameGroupModelAdminGroup)
modeladmin_register(BlogArticleModelAdmin)

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


@hooks.register('register_image_operations')
def register_image_operations():
    return [
        ('pad', PadOperation),
    ]
