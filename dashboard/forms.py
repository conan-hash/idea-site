from django import forms
from .models import Idea, Proposal, Contributor
from django.forms import inlineformset_factory

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
        fields = [
            'projectType', 'research_pole', 'research_pole_username',
            'developer', 'costumer', 'nameAndNumberofPlan'
        ]
        widgets = {
            'projectType': forms.Select(attrs={'class': 'form-select', 'dir': 'rtl'}),
            'research_pole': forms.Select(attrs={'class': 'form-select', 'dir': 'rtl'}),
            'research_pole_username': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
            'developer': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
            'costumer': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
            'nameAndNumberofPlan': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
            'first_nameAndLast_name': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
            'work_place': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
            'major': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
            'work_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'dir': 'rtl'}),
            'job': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
            'work_phone': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
        }



class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['judge1_score', 'judge2_score', 'judge3_score', 'judge4_score']
        widgets = {
            'judge1_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 20}),
            'judge2_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 20}),
            'judge3_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 20}),
            'judge4_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 20}),
        }



class ContributorForm(forms.ModelForm):
    class Meta:
        model = Contributor
        fields = ['name', 'contribution_percent_idea', 'contribution_percent_project']

ContributorFormSet = inlineformset_factory(
    Idea,                      
    Contributor,             
    form=ContributorForm,      
    extra=1,                   
    can_delete=False,          
)
