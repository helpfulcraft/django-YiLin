from django import forms
from .models import VolunteerActivity, VolunteerApplication
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ActivityForm(forms.ModelForm):
    """活动表单"""
    class Meta:
        model = VolunteerActivity
        fields = ['title', 'description', 'category', 'image', 'location', 
                 'start_time', 'end_time', 'required_volunteers', 'status']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', '提交'))

class ApplicationForm(forms.ModelForm):
    """报名表单"""
    class Meta:
        model = VolunteerApplication
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', '申请'))
