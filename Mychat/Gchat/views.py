from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, FormView, RedirectView
from .forms import *
from .models import *

from django.template.loader import render_to_string
from django.contrib.auth import login, logout, authenticate


class index(View):
    template_name = 'index.html'
    form_class = roomForm

    def get(self, request, *args, **kwargs):
        form = roomForm()
        rooms = roomModel.objects.filter(pk__lt=14)
        return render(request, 'index.html', {'form': form, 'rooms': rooms})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            room_name = form.cleaned_data['room_name']
            try:
                name = roomModel.objects.get(room_name=room_name)
                return HttpResponseRedirect('/chat/' + room_name)
            except:
                return HttpResponseRedirect('/chat/')
        return HttpResponseRedirect('/chat/')


def room(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name
    })

class Registration(CreateView):
    template_name = 'registration.html'
    success_url = reverse_lazy('index')
    form_class = UserRegistrationForm
    object_list = []

    def form_valid(self, form):
        valid = super(Registration, self).form_valid(form)
        username = self.request.POST['username']
        password = self.request.POST['password1']
        userauth = authenticate(self.request,username=username,password=password)
        if userauth is not None:
            login(self.request, userauth)
        return valid

class Logout(RedirectView):
    url = reverse_lazy('login')
    def get(self, *args, **kwargs):
        logout(self.request)
        return super(Logout, self).get(self, *args, **kwargs)


class Login(FormView):
    template_name = 'login.html'
    success_url = reverse_lazy('index')
    form_class = UserLoginForm

    def form_valid(self, form):
        username = self.request.POST['username']
        password = self.request.POST['password']
        userauth = authenticate(self.request,username=username,password=password)
        if userauth is not None:
             if userauth.is_active:
                 login(self.request, userauth)
        return super(Login, self).form_valid(form)


class CreateRoom(CreateView):
    template_name = 'createroom.html'
    success_url = reverse_lazy('index')
    form_class = roomForm
    object_list = []

    def form_valid(self, form):
        valid = super(CreateRoom, self).form_valid(form)
        return valid