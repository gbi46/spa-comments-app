from .captcha import CaptchaUtil
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Comment
from .utils import CommentSerializer, CommentUtil
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic.edit import CreateView
from .models import Comment
from .forms import CommentForm
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import logging

logger = logging.getLogger(__name__)

class AddCommentView(APIView):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                email = request.POST.get('email')
                text = request.POST.get('text')

                logger.info(f'Получен новый комментарий от {email}')

                user = User.objects.filter(email=email).first()

                if not user:
                    user = User.objects.create_user(username=email, email=email)

                comment = Comment(text=text, email=email)
                comment.user = user
                comment.save()

                logger.info(f'Комментарий от {email} успешно добавлен.')

                return JsonResponse({
                    'status': 'success',
                    'message': 'Комментарий успешно добавлен.',
                    'comment_text': comment.text,
                    'user': comment.user.username,
                })
            except Exception as e:
                logger.error(f'Ошибка добавления комментария: {e}')
                return JsonResponse({
                    'status': 'error',
                    'message': 'Ошибка добавления комментария.',
                })

        return JsonResponse({
            'status': 'error',
            'message': 'Неверный запрос.',
        })


class CommentsView(View):
    template_name = 'comments/comments.html'

    def get(self, request):

        comments = Comment.objects.all()
        return render(request, self.template_name, {'comments': comments})

    def form_valid(self, form):
            user_name = form.cleaned_data['user_name']
            email = form.cleaned_data['email']
            home_page = form.cleaned_data['home_page']
            captcha = form.cleaned_data['captcha']
            text = form.cleaned_data['text']

            CommentUtil.add_comment(user_name, email, home_page, captcha, text)
            return super().form_valid(form)

def get_captcha(request):
    captcha_text, image_bytes = CaptchaUtil.generate_captcha()
    request.session['captcha_text'] = captcha_text
    captcha_image = CaptchaUtil.get_image(image_bytes)
    
    return JsonResponse({'image': captcha_image})

