from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.urls import reverse_lazy

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Word
from django.contrib.auth.models import User
from .serializers import *


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('words')


class CustomRegisterView(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('words')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(CustomRegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('words')
        return super(CustomRegisterView, self).get(*args, **kwargs)


class ProfileView(LoginRequiredMixin, ListView):
    model = Word
    context_object_name = 'words'
    template_name = 'base/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {
            'words': context['words'].filter(user=self.request.user),
            'learned_words': len(context['words'].filter(complete=True)),
            'not_learned_words': len(context['words'].filter(complete=False)),
        }
        return context


class AboutView(LoginRequiredMixin, ListView):
    model = Word
    context_object_name = 'words'
    template_name = 'base/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {
            'words': context['words'],
            'words_count': len(context['words']),
            'users_count': len(set([word.user for word in context['words']])),
        }
        return context


class WordList(LoginRequiredMixin, ListView):
    model = Word
    context_object_name = 'words'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['words'] = context['words'].filter(user=self.request.user)
        return context


class WordDetail(LoginRequiredMixin, DetailView):
    model = Word
    context_object_name = 'word'
    template_name = 'base/word.html'


class WordCreate(LoginRequiredMixin, CreateView):
    model = Word
    fields = ['english', 'ukrainian', 'examples']
    # fields = '__all__'
    success_url = reverse_lazy('words')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(WordCreate, self).form_valid(form)


class WordUpdate(LoginRequiredMixin, UpdateView):
    model = Word
    fields = ['english', 'ukrainian', 'examples', 'complete']
    success_url = reverse_lazy('words')


class WordDelete(LoginRequiredMixin, DeleteView):
    model = Word
    context_object_name = 'word'
    success_url = reverse_lazy('words')


@api_view(['GET'])
def apiOverview(requset):
    api_urls = {
        "Words": 'api/word/',
        'Words details': 'api/word/<int:pk>',
        'Create': 'api/word-create/',
        'Update': 'api/word-update/<int:pk>',
        'Delete': 'api/word-delete/<int:pk>',
    }
    return Response(api_urls)


@api_view(['GET'])
def wordList(request):
    words = Word.objects.all().order_by('id')
    serializer = WordListSerializer(words, many=True, )
    print(serializer)
    return Response(serializer.data)


@api_view(['GET'])
def wordDetail(request, pk):
    words = Word.objects.get(id=pk)
    serializer = WordDetailSerializer(words, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def wordCreate(request):
    serializer = WordCreateSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def wordUpdate(request, pk):
    word = Word.objects.get(id=pk)
    serializer = WordDetailSerializer(instance=word, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def wordDelete(request, pk):
    word = Word.objects.get(id=pk)
    word.delete()

    return Response("Item successfully deleted")
