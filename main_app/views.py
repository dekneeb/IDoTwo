from pdb import post_mortem
from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from .models import Item

# Create your views here.

class Home(TemplateView):
    template_name='home.html'

class About(TemplateView):
    template_name='about.html'

class ItemCreate(CreateView):
    model = Item
    fields = ['title', 'img', 'location', 'description', 'price', 'shipping']
    template_name = 'create_post.html'
    success_url = ''

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ItemCreate, self).form_valid(form)
