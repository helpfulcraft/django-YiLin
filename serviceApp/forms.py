from django import forms
from .models import ServiceAppointment, ServiceReview

class ServiceAppointmentForm(forms.ModelForm):
    """服务预约表单"""
    class Meta:
        model = ServiceAppointment
        fields = ['appointment_time', 'note']
        widgets = {
            'appointment_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'note': forms.Textarea(attrs={'rows': 4}),
        }

class ServiceReviewForm(forms.ModelForm):
    """服务评价表单"""
    class Meta:
        model = ServiceReview
        fields = ['rating', 'content']
        widgets = {
            'rating': forms.RadioSelect(),
            'content': forms.Textarea(attrs={'rows': 4}),
        }
