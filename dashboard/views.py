from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Idea 
import json
import datetime
# Create your views here.

def track_idea(request, identifier):
    idea = get_object_or_404(Idea, identifier=identifier)
    return render(request, 'track-idea.html', {'idea': idea})


def submit_new_idea(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.user = request.user
            idea.date = datetime.date.today()
            idea.status = 'pending'
            idea.save()
            request.session['identifier'] = idea.identifier
            return redirect('successful') 
    else:
        form = IdeaForm()

    return render(request, 'new.html', {'form': form})


def user_ideas(request):
    ideas = Idea.objects.filter(user=request.user).order_by('-date')
    return render(request, 'user-ideas.html', {'ideas': ideas})


def user_profile(request):
    context = {
		'user': request.user
    }
    return render(request, 'users-profile.html', context)


def referee(request):
    ideas = Idea.objects.filter(judge1=request.user).order_by('-date')
    return render(request, 'user-ideas.html', {'ideas': ideas})

def all_ideas(request):
    ideas = Idea.objects.all().order_by('-date')
    return render(request, 'user-ideas.html', {'ideas': ideas})

def successful(request):
    identifier = request.session.pop('identifier', None)  
    return render(request, 'successful.html', {'identifier': identifier})