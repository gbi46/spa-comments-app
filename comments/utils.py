from .captcha import CaptchaUtil
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
            captcha_text, image_bytes = CaptchaUtil.generate_captcha()
            request.session['captcha_text'] = captcha_text
            captcha_image = CaptchaUtil.get_image(image_bytes)
            
            return render(request, 'comments/add_comment.html', {'captcha_image': captcha_image})

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'user_name', 'email', 'home_page', 'parent', 'created_at']
