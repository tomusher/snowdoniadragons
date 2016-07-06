import json

from wagtail.wagtailcore.blocks import CharBlock, StructBlock, StreamBlock, PageChooserBlock, URLBlock, ChoiceBlock
from django.template.loader import render_to_string

from base.models import Game

class SelectizeGameBlock(CharBlock):
    def render_form(self, value, prefix='', errors=None):
        widget = self.field.widget

        try:
            game = Game.objects.get(bgg_id=value)
            widget_attrs = {'id': prefix, 'placeholder': self.label, 'data-name': game.name}
        except Game.DoesNotExist:
            widget_attrs = {'id': prefix, 'placeholder': self.label}

        field_value = self.value_for_form(value)

        if hasattr(widget, 'render_with_errors'):
            widget_html = widget.render_with_errors(prefix, field_value, attrs=widget_attrs, errors=errors)
            widget_has_rendered_errors = True
        else:
            widget_html = widget.render(prefix, field_value, attrs=widget_attrs)
            widget_has_rendered_errors = False

        return render_to_string('wagtailadmin/block_forms/field.html', {
            'name': self.name,
            'classes': self.meta.classname,
            'widget': widget_html,
            'field': self.field,
            'errors': errors if (not widget_has_rendered_errors) else None
        })

class GameBlock(StructBlock):
    game = SelectizeGameBlock()
    times_played = CharBlock(required=False)
    game_object_pk = CharBlock(required=False)

    def get_prep_value(self, value):
        prep_value = super().get_prep_value(value)
        game, created = Game.objects.get_or_create(bgg_id=prep_value['game'])
        prep_value.update({
            'game_object_pk': game.pk
        })
        return prep_value


