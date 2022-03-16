
# from xml.etree.ElementTree import Comment
from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from .models import Item, Comment, ThreadModel, MessageModel, UserProfile, Notification
from .forms import CommentForm, SignUpForm, ThreadForm, MessageForm
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.models import User
# from django.dispatch import receiver



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
            context['header'] = "I Do Two's"
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 

        city = self.request.GET.get('city')

        if city != None:
            context['items'] = Item.objects.filter(city__icontains=city)
            context['header'] = f"Results for {city}"
        else:
            context['items'] = Item.objects.all()
            context['header'] = "I Do Two's"
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
    form_class= CommentForm
    template_name = 'add_comment.html'
    success_url = reverse_lazy('items_list')

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.name = self.request.user

        # notification = Notification.objects.create(notification_type=2, from_user=self.request.user, to_user=Comment.post.user, post=Comment.post)

        return super().form_valid(form)

        


class UserEditView(UpdateView):
    form_class=UserChangeForm
    template_name='registration/edit_profile.html'
    succes_url=reverse_lazy('items_list')

    def get_object(self):
        return self.request.user


class Profile(TemplateView):
    template_name='profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 

        
        title = self.request.GET.get('title')
        print(title)
        if title != None:
            context['items'] = Item.objects.filter(title__icontains=title)
            context['header'] = f"Results for {title}"
        else:
            context['items'] = Item.objects.all()
            context['header'] = "I Do Two's"
        return context





class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))

        context = {
            'threads' : threads
        }
        return render(request, 'inbox.html', context)
    
class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()
        context = {
            'form' : form
        }
        return render(request, 'createthread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        username = request.POST.get('username')

        try: 
            receiver = User.objects.get(username =username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect ('thread', pk=thread.pk)
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect ('thread', pk=thread.pk)

            if form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                    )
                print(thread)
                thread.save()

            return redirect('thread', pk=thread.pk)

        except:
            return redirect('createthread')

class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form =MessageForm() 
        thread = ThreadModel.objects.get(pk=pk)
        message_list=MessageModel.objects.filter(thread__pk__contains=pk)
      
        context ={
            'thread' : thread,
            'form' : form,
            'message_list' : message_list
        }

        return render(request, 'thread.html', context)

class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver
        print(receiver)
        message=MessageModel(
            thread=thread,
            sender_user = request.user,
            receiver_user = receiver,
            body=request.POST.get('message')
        )

        message.save()

        notification = Notification.objects.create(
            notification_type=1,
            from_user = request.user,
            to_user = receiver,
            thread=thread
            )

        return redirect('thread', pk=pk)

class PostNotification(View):
    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Item.objects.get(pk = post_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('post_detail', pk=post_pk)

class ThreadNotification(View):
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        thread = ThreadModel.objects.get(pk = object_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('thread', pk=object_pk)




