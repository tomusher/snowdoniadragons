from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from boardgamegeek import BoardGameGeek

from base.models import Game
from group.models import Group
from session.models import Session
from blog.models import BlogArticle

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(*args, **kwargs):
        return {
            'groups': Group.objects.all(),
            'upcoming_sessions': Session.objects.filter(date__gte=datetime.now()),
            'recent_sessions': Session.objects.filter(date__lt=datetime.now())[:10],
            'blog_posts': BlogArticle.objects.all()[:10]
        }

class SearchGamesView(TemplateView):
    def render_to_response(self, context, **response_kwargs):
        result_dict = [{'id': game.bgg_id, 'name': game.name} for game in Game.objects.all()]
        bgg = BoardGameGeek()
        results = bgg.search(
            self.request.GET.get('query'),
            search_type = ['boardgame']
        )
        result_dict = result_dict + [{'id': r.id, 'name': r.name} for r in results]
        filtered_results = list(dict((v['id'], v) for v in result_dict).values())
        return JsonResponse(
            {"results": filtered_results}
        )


