from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from boardgamegeek import BoardGameGeek

from .models import Session

class SearchGamesView(TemplateView):
    def render_to_response(self, context, **response_kwargs):
        bgg = BoardGameGeek()
        results = bgg.search(
            self.request.GET.get('query'),
            search_type = ['boardgame']
        )
        result_dict = [{'id': r.id, 'name': r.name} for r in results]
        print(result_dict)
        return JsonResponse(
            {"results": result_dict}
        )
