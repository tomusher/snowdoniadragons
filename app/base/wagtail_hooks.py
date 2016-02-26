from django.utils.html import format_html, format_html_join
from django.conf import settings

from wagtail.wagtailcore import hooks
from wagtailmodeladmin.options import ModelAdmin, wagtailmodeladmin_register

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

class BlogArticleModelAdmin(ModelAdmin):
    model = BlogArticle
    menu_label = 'Blog Post'
    list_display = ('title',)
    search_fields = {'title',}

wagtailmodeladmin_register(SessionModelAdmin)
wagtailmodeladmin_register(GroupModelAdmin)
wagtailmodeladmin_register(BlogArticleModelAdmin)

@hooks.register('insert_editor_js')
def selectize_js():
    js_files = [
        'js/admin/selectize.js',
        'js/admin/admin.js'
    ]

    js_includes = format_html_join('\n', '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )

    return js_includes

@hooks.register('insert_editor_css')
def selectize_css():
    css_files = [
        'css/admin/selectize.css',
        'css/admin/selectize.bootstrap3.css'
    ]

    css_includes = format_html_join('\n', '<link rel="stylesheet" href="{0}{1}">',
        ((settings.STATIC_URL, filename) for filename in css_files)
    )

    return css_includes

@hooks.register('construct_main_menu')
def construct_main_menu(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name not in ('explorer')]
