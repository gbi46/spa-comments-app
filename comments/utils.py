from django.http import HttpResponse, HttpResponseRedirect
from PIL import Image, ImageDraw, ImageFont
from rest_framework import serializers
from .models import Comment
import random, string
from io import BytesIO
from django.shortcuts import render, redirect
from django.urls import reverse
from captcha.image import ImageCaptcha

class CommentUtil:
    def generate_captcha(request):
        # Генерация случайного текста для капчи (можно использовать буквы и цифры)
        captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        # Создание изображения капчи
        image = ImageCaptcha(width=160, height=60)
        
        # Генерация изображения с текстом капчи
        image_data = image.generate(captcha_text)

        # Преобразуем изображение в HTTP-ответ
        response = HttpResponse(image_data, content_type="image/png")
        
        # Сохраняем капчу в сессии для дальнейшей валидации
        request.session['captcha'] = captcha_text
        
        return response

    def check_captcha(request):
        user_captcha = request.POST.get('captcha')
        session_captcha = request.session.get('captcha')
        
        if user_captcha and user_captcha.lower() == session_captcha.lower():
            # Капча введена верно
            # Обрабатываем остальные данные формы
            return HttpResponse("Форма отправлена успешно!")
        else:
            # Неверная капча
            return HttpResponse("Неверный код с картинки. Попробуйте снова.")


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
