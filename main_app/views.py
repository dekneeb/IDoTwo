from pdb import post_mortem
from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from .models import Item, Photo
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import uuid
import boto3

# Create your views here.

class Home(TemplateView):
    template_name='home.html'

class About(TemplateView):
    template_name='about.html'

class ItemCreate(CreateView):
    model = Item
    fields = ['title', 'img', 'city', 'description', 'price', 'shipping']
    template_name = 'create_post.html'
    success_url = '/items/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ItemCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk' : self.object.pk})

# @method_decorator(login_required)
class ItemList(TemplateView):
    template_name='items_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 

        title = self.request.GET.get('title')
        print(title)
        if title != None:
            context['items'] = Item.objects.filter(title__icontains=title)
            context['header'] = f"Results for {title}"
        else:
            context['items'] = Item.objects.all()
            context['header'] = "Trending Items"
        return context


class PostDetail(DetailView):
    model = Item
    template_name= 'post_detail.html'

class PostUpdate(UpdateView):
    model = Item
    fields = ['title', 'img', 'city', 'description', 'price', 'shipping']
    template_name = 'post_update.html'
    success_url = '/items/'

class PostDelete(DeleteView):
    model = Item
    template_name = "post_delete.html"
    success_url='/items/'


class Signup(View):
    def get(self,request):
        form = UserCreationForm()
        context = {"form" : form }
        return render(request, "registration/signup.html", context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user=form.save()
            login(request, user)
            return redirect('items_list')
        else:
            context = {"form" : form}
            return render(request, "registartion/signup.html", context)

class AddPhoto():
    