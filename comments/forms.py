from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    user_name = forms.CharField(max_length=100, required=True, label="Пользователь")
    email = forms.EmailField(required=True, label="E-mail")
    home_page = forms.URLField(required=False, label="Веб страница")
    file = forms.FileField(required=False, label="Файл")
    text = forms.CharField(widget=forms.Textarea, required=True, label="Комментарий")
    captcha = forms.CharField(max_length=6, required=True, label="Введите код с картинки")

    class Meta:
        model = Comment
        fields = ['file', 'text', 'user_name', 'email', 'home_page', 'captcha', 'parent']

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        if not user_name.isalnum():
            raise forms.ValidationError("Имя пользователя может содержать только латинские буквы и цифры.")
        return user_name

    def clean_captcha(self):
        entered_text = self.cleaned_data.get('captcha').lower()
        correct_text = self.request.session.get("captcha").lower()

        if entered_text != correct_text:
            raise forms.ValidationError(f"Неверный код капчи!")

        return entered_text
