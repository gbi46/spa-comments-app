from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont
from rest_framework import serializers
from .models import Comment
import random, string
from io import BytesIO
from django.shortcuts import render, redirect

class CommentUtil:
    def create_captcha_image(self):
        # Генерирует картинку с капчей
        text = self.generate_captcha()
        
        image = Image.new('RGB', (150, 50), 'white')
        draw = ImageDraw.Draw(image)
        
        # Используем стандартный шрифт, если нет TTF-файла
        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except IOError:
            font = ImageFont.load_default()
        
        draw.text((20, 10), text, font=font, fill='black')

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

    def generate_captcha(self):
        # Генерация текста капчи
        captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        # Создание изображения капчи
        image = Image.new('RGB', (120, 40), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        draw.text((10, 10), captcha_text, font=font, fill=(0, 0, 0))

        # Преобразование изображения в байты
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        image_bytes = buffer.getvalue()

        # Возвращаем изображение в HttpResponse
        return HttpResponse(image_bytes, content_type="image/png")

    def get_all_comments():
        return Comment.objects.all()

    def add_comment(request):
        if request.method == 'POST':
            user_name = request.POST['user_name']
            email = request.POST['email']
            home_page = request.POST['home_page']
            captcha = request.POST['captcha']
            text = request.POST['text']

            # Проверка капчи
            if captcha == request.session.get('captcha_text'):
                Comment.objects.create(user_name=user_name, email=email, home_page=home_page, captcha=captcha, text=text)
                return redirect('comments:comments_list')
            else:
                return render(request, 'comments/add_comment.html', {'error': 'Неверная капча'})
        else:
            captcha_text, image_bytes = self.generate_captcha()
            request.session['captcha_text'] = captcha_text
            captcha_image = f"data:image/png;base64,{image_bytes.decode('latin1')}"
            return render(request, 'comments/add_comment.html', {'captcha_image': captcha_image})

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'user_name', 'email', 'home_page', 'parent', 'created_at']
