from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from boardgamegeek import BoardGameGeek

from base.models import Game
from group.models import Group
from blog.models import BlogArticle

class SearchGamesView(TemplateView):
    def render_to_response(self, context, **response_kwargs):
        bgg = BoardGameGeek()
        results = bgg.search(
            self.request.GET.get('query'),
            search_type = ['boardgame']
        )
        result_dict = [{'id': 'bgg_{0}'.format(r.id), 'name': "{0} ({1})".format(r.name, r.year)} for r in results]
        filtered_results = list(dict((v['id'], v) for v in result_dict).values())
        return JsonResponse(
            {"results": filtered_results}
        )


