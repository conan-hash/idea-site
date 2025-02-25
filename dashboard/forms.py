from django import forms
from .models import Idea, Proposal

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['title', 'goal', 'importance', 'details', 'date', 'identifier']
        widgets = {
        'title' : forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
        'goal' : forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
        'importance' : forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
        'details' : forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
        'date' : forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
        'identifier' : forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
    }
        

class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal  
        fields = [
            'titleFa', 'titleEn', 'keyWords', 'projectType', 'research_pole', 'research_pole_username',
            'developer', 'costumer', 'nameAndNumberofPlan'
        ]
        widgets = {
            'titleFa': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
            'titleEn': forms.TextInput(attrs={'class': 'form-control'}),
            'keyWords': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'dir': 'rtl'}),
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



