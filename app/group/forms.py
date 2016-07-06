from django import forms

from wagtail.wagtailadmin.forms import WagtailAdminPageForm

from base.models import Game

class GameChoiceField(forms.ModelChoiceField):
    def to_python(self, value):
        if value in self.empty_values:
            return None

        if value.startswith('bgg_'):
            bgg_id = value[4:]
            game, created = Game.objects.get_or_create(bgg_id=bgg_id)
            return game

        return self.queryset.get(**{'pk': value})

class SessionForm(WagtailAdminPageForm):
    def __init__(self, data=None, files=None, parent_page=None, *args, **kwargs):
        super().__init__(data, files, parent_page, *args, **kwargs)
        games_played = self.formsets['games_played']
        try:
            for subform in games_played.forms:
                subform.fields['game'] = GameChoiceField(queryset=Game.objects.all())
        except:
            pass

