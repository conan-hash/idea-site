from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.shortcuts import render
from .models import Idea 
import datetime
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash


# Create your views here.
@login_required
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

@login_required
def user_ideas(request):
    ideas = Idea.objects.filter(user=request.user).order_by('-date')
    return render(request, 'user-ideas.html', {'ideas': ideas})

@login_required
def user_profile(request):
    if request.method == 'POST':
        if 'changepass' in request.POST:
            passwordform = CustomPasswordChangeForm(request.user, request.POST)
            if passwordform.is_valid():
                user = passwordform.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('user_profile') 
    else:
        passwordform = CustomPasswordChangeForm(request.user)
    context = {
        'user': request.user,
        'passwordform': passwordform
        }
    return render(request, 'users-profile.html', context)

@login_required
def referee(request):
    ideas = Idea.objects.filter(evaluations__judge=request.user).order_by('-date')
    return render(request, 'user-ideas.html', {'ideas': ideas})

@login_required
def all_ideas(request):
    ideas = Idea.objects.all().order_by('-date')
    return render(request, 'user-ideas.html', {'ideas': ideas})

@login_required
def successful(request):
    identifier = request.session.pop('identifier', None)  
    return render(request, 'successful.html', {'identifier': identifier})

@login_required
def track_idea(request, identifier):
    idea = Idea.objects.get(identifier=identifier)
    presentation, created = Presentation.objects.get_or_create(idea=idea)
    is_submitter = request.user == idea.user
    is_judge = JudgeEvaluation.objects.filter(idea=idea, judge=request.user).exists()
    is_employee = request.user.groups.filter(name='employee').exists()

    if is_submitter:
        if request.method == 'POST':
            user_presentation_form = UserPresentationForm(request.POST, request.FILES, instance=presentation)
            if user_presentation_form.is_valid():
                user_presentation_form.save()
                return redirect('track_idea', identifier=idea.identifier)
        else:
            user_presentation_form = UserPresentationForm(instance=presentation)

        # If it's a submitter, the form will allow uploading the presentation file.
        return render(request, 'track-idea.html', {
            'idea': idea,
            'presentation': presentation,
            'user_presentation_form': user_presentation_form,
            'is_submitter': is_submitter,
        })

    elif is_judge:
        if request.method == 'POST':
            evaluation_form = EvaluationForm(request.POST, instance=presentation)
            if evaluation_form.is_valid():
                evaluation_form.save()
                return redirect('track_idea', identifier=idea.identifier)
        else:
            evaluation_form = EvaluationForm(instance=presentation)

        return render(request, 'track_idea.html', {
            'idea': idea,
            'presentation': presentation,
            'evaluation_form': evaluation_form,
            'is_judge': is_judge,
        })

    elif is_employee:
        if request.method == 'POST':
            if "date" in request.POST:
                employee_presentation_form = EmployeePresentationForm(request.POST, instance=presentation)
                if employee_presentation_form.is_valid():
                    employee_presentation_form.save()
                    return redirect('track_idea', identifier=idea.identifier)
            if "confirm" in request.POST:
                confirm = request.POST.get("approve_grades")
                if confirm == "on":
                    presentation.approved = True
                presentation.save()
                return redirect('track_idea', identifier=idea.identifier)
            if "firstconfirm" in request.POST:
                if idea.status == "pending":
                    confirm = request.POST.get("approval")
                    if confirm == "yes":
                        idea.status = "proposal"
                    if confirm == "no":
                        idea.status = "rejected"
                    idea.save()
                return redirect('track_idea', identifier=idea.identifier)
        else:
            employee_presentation_form = EmployeePresentationForm(instance=presentation)

        return render(request, 'track-idea.html', {
            'idea': idea,
            'presentation': presentation,
            'employee_presentation_form': employee_presentation_form,
            'is_employee': is_employee,
        })

    else:
        return HttpResponse('Unauthorized', status=403)

