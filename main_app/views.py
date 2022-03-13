from pdb import post_mortem
import re
# from xml.etree.ElementTree import Comment
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from .models import Item, Comment
from .forms import CommentForm, SignUpForm
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import uuid
import boto3
import os
from django.http import HttpResponseRedirect


# Create your views here.

class Home(TemplateView):
    template_name='home.html'

class About(TemplateView):
    template_name='about.html'

class ItemCreate(CreateView):
    model = Item
    fields = ['title', 'city', 'description', 'price', 'shipping', 'photos']
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
    fields = ['title', 'city', 'description', 'price', 'shipping']
    template_name = 'post_update.html'
    success_url = '/items/'

class PostDelete(DeleteView):
    model = Item
    template_name = "post_delete.html"
    success_url='/items/'


class Signup(View):
    def get(self,request):
        form = SignUpForm()
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
            return render(request, "registration/signup.html", context)


class AddCommentView(CreateView):
    model = Comment
    template_name = 'add_comment.html'
    success_url = reverse_lazy('items_list')
    fields = '__all__'

    def form_valid(self, form):
        form.instance.item_id = self.kwargs['pk']
        return super().form_valid(form)


class UserEditView(UpdateView):
    form_class=UserChangeForm
    template_name='registration/edit_profile.html'
    succes_url=reverse_lazy('items_list')

    def get_object(self):
        return self.request.user


class Profile(TemplateView):
    template_name='profile.html'
    


