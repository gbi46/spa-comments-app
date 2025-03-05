from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    captcha = CaptchaField(label="Введите код с картинки")
    
    class Meta:
        model = Comment
        fields = ['text', 'user_name', 'email', 'home_page', 'captcha', 'parent']

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        if not user_name.isalnum():
            raise forms.ValidationError("User Name может содержать только латинские буквы и цифры.")
        return user_name

    def clean_captcha(self):
        """Здесь нужно реализовать проверку CAPTCHA, например, через сессию"""
        captcha = self.cleaned_data.get('captcha')
    
        if captcha.lower() != 'abc123':
            raise forms.ValidationError("Неверный код CAPTCHA.")
        return captcha
