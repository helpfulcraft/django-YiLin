from django import forms
from .models import News, NewsComment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class NewsForm(forms.ModelForm):
    """新闻表单"""
    
    class Meta:
        model = News
        fields = ['title', 'category', 'cover', 'summary', 'content', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入新闻标题'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'cover': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '请输入新闻摘要'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': '请输入新闻内容'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            })
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "请选择分类"
        
        # 添加帮助文本
        self.fields['title'].help_text = '标题应简明扼要，建议不超过50个字'
        self.fields['summary'].help_text = '摘要会显示在新闻列表中，建议100字以内'
        self.fields['content'].help_text = '支持基本的文本格式'
        self.fields['status'].help_text = '草稿状态的新闻不会显示在前台'
        
        # 添加表单助手
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', '保存'))
        
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) > 100:
            raise forms.ValidationError('标题长度不能超过100个字符')
        return title
        
    def clean_summary(self):
        summary = self.cleaned_data.get('summary')
        if len(summary) > 300:
            raise forms.ValidationError('摘要长度不能超过300个字符')
        return summary

class NewsCommentForm(forms.ModelForm):
    """新闻评论表单"""
    class Meta:
        model = NewsComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '请输入评论内容'
            })
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', '发表评论'))
        
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 5:
            raise forms.ValidationError('评论内容不能少于5个字符')
        return content
