from django import forms
from .models import Idea, Proposal, Presentation, JudgeEvaluation
from django.forms import inlineformset_factory
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['title', 'goal', 'importance', 'details', 'keywords']
        widgets = {
        'title' : forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
        'keywords': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
        'goal' : forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
        'importance' : forms.Textarea(attrs={'class': 'form-control', 'dir': 'rtl'}),
        'details' : forms.Textarea(attrs={'class': 'form-control', 'dir': 'rtl'}),
    }
        

class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal  
        fields = ['projectType']




class UserPresentationForm(forms.ModelForm):
    class Meta:
        model = Presentation
        fields = ['presentation_file']

    def clean_presentation_file(self):
        file = self.cleaned_data.get('presentation_file')
        if file and file.size > 10 * 1024 * 1024:  # 10 MB size limit for the file
            raise ValidationError("فایل ارائه باید کمتر از ۱۰ مگابایت باشد.")
        return file

class EmployeePresentationForm(forms.ModelForm):
    class Meta:
        model = Presentation
        fields = ['presentation_time']
        widgets = {
        'presentation_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
    def clean_presentation_date(self):
        date = self.cleaned_data.get('presentation_date')
        if date and date < timezone.now().date():
            raise ValidationError("تاریخ ارائه باید از امروز بعد باشد.")
        return date

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = JudgeEvaluation
        fields = ['score', 'comment']

    def clean_score(self):
        score = self.cleaned_data.get('score')
        if not (1 <= score <= 20):
            raise ValidationError("امتیاز باید بین 1 و 20 باشد.")
        return score


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})


