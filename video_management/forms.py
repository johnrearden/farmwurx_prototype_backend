from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class TaskForm(forms.Form):
    """
    Form for creating tasks from videos
    """
    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task name'})
    )
    
    taskee = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Assign To'
    )
    
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Describe what needs to be done in this task'
        })
    )
    
    due_date = forms.DateTimeField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Select due date and time',
        }),
        input_formats=['%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S'],
    )
    
    include_video = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Link video to task'
    )
    
    include_transcription = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Include video transcription in description'
    )
    
    def clean_due_date(self):
        """
        Validate that due date is not in the past
        """
        due_date = self.cleaned_data.get('due_date')
        
        if due_date and due_date < forms.utils.timezone.now():
            raise ValidationError(_('Due date cannot be in the past'))
            
        return due_date
