from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    """用户注册表单"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被注册')
        return email

class UserProfileForm(forms.ModelForm):
    """用户资料表单"""
    class Meta:
        model = UserProfile
        fields = ('avatar', 'bio')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
