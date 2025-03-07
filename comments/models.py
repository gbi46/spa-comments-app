from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
import bleach
import re
import os

def validate_image(image):
    width, height = get_image_dimensions(image)
    valid_formats = ['image/jpeg', 'image/gif', 'image/png']

    if image.content_type not in valid_formats:
        raise ValidationError("Недопустимый формат изображения. Допустимые форматы: JPG, GIF, PNG.")
    
    if width > 320 or height > 240:
        raise ValidationError("Изображение не должно превышать 320x240 пикселей.")

    if width > 320 or height > 240:
        from PIL import Image
        img = Image.open(image)
        img.thumbnail((320, 240))
        img.save(image.path)

def validate_txt_file(file):
    if file.size > 100 * 1024:
        raise ValidationError("Текстовый файл не должен превышать 100 КБ.")

    if not file.name.endswith('.txt'):
        raise ValidationError("Файл должен быть в формате .txt.")

class Comment(models.Model):
    file = models.FileField(upload_to='uploads/', null=True, blank=True, validators=[validate_image, validate_txt_file])
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

    def save(self, *args, **kwargs):
        self.text = bleach.clean(self.text, tags=['i', 'a', 'code', 'strong'], attributes={'a': ['href', 'title']})
        super().save(*args, **kwargs)

