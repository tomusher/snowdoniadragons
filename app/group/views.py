from django.shortcuts import render

from django.views.generic import DetailView, TemplateView

from .models import Group

class GroupDetailView(DetailView):
    model = Group
    template_name = "group.html"

class GalleryView(TemplateView):
    template_name = "gallery.html"
    def get_context_data(self, **kwargs):
        group = Group.objects.get(slug=kwargs['slug'])
        return {
            'group': group,
            'images': group.all_images
        }
