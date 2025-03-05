from django.db import models

from django.db import models
from django.contrib.auth.models import User
import re
from django.core.exceptions import ValidationError

class Comment(models.Model):
    text = models.TextField()
    user_name = models.CharField(max_length=100)
    email = models.EmailField()
    home_page = models.URLField(blank=True, null=True)
    captcha = models.CharField(max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Комментарий от {self.user_name} на {self.created_at}"

    def clean(self):
        if not re.match(r'^[A-Za-z0-9]+$', self.captcha):
            raise ValidationError('Капча должна содержать только латинские буквы и цифры.')

        if not re.match(r'^[A-Za-z0-9]+$', self.user_name):
            raise ValidationError('Имя пользователя должно содержать только латинские буквы и цифры.')

        if any(tag in self.text for tag in ['<', '>']):
            raise ValidationError('HTML теги не допускаются в тексте комментария, за исключением разрешённых.')

        super().clean()

