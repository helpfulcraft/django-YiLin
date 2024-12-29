from django import forms
from .models import Activity, Application

class ActivityForm(forms.ModelForm):
    """志愿活动表单"""
    class Meta:
        model = Activity
        fields = ['title', 'description', 'date', 'location', 'volunteers_needed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'volunteers_needed': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ApplicationForm(forms.ModelForm):
    """志愿申请表单"""
    class Meta:
        model = Application
        fields = ['apply_reason']
        widgets = {
            'apply_reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '请简要说明您参加此次志愿活动的原因...'
            }),
        }
