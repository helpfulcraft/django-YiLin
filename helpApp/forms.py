from django import forms
from .models import Feedback, OnlineConsultation

class FeedbackForm(forms.ModelForm):
    """反馈表单"""
    class Meta:
        model = Feedback
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入反馈标题'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': '请详细描述您的问题或建议'}),
        }

class ConsultationForm(forms.ModelForm):
    """咨询表单"""
    class Meta:
        model = OnlineConsultation
        fields = ['category', 'title', 'content']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入咨询标题'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': '请详细描述您的咨询内容'}),
        }
