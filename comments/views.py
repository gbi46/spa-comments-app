from .captcha import CaptchaUtil
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Comment
from .utils import CommentSerializer, CommentUtil
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import CreateView
from .models import Comment
from .forms import CommentForm
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import logging

logger = logging.getLogger(__name__)

@method_decorator(csrf_protect, name='dispatch')
class AddCommentView(APIView):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = CommentForm(request.POST or None, request.FILES, request=request)
            if form.is_valid():
                comment = form.save()
                try:
                    email = request.POST.get('email')
                    text = request.POST.get('text')
                    user_name = request.POST.get('user_name')
                    home_page = request.POST.get('home_page')
                    if request.POST.get('parent_comment_id'):
                        parent_comment_id = request.POST.get('parent_comment_id')
                    else:
                        parent_comment_id = None

                    if not CaptchaUtil.check_captcha(request):
                        return JsonResponse({
                            'status': 'error',
                            'message': 'Неверный код капчи.'
                        })

                    logger.info(f'Получен новый комментарий от {email}')

                    user = User.objects.filter(email=email).first()

                    if not user:
                        user = User.objects.create_user(email=email, username=user_name)

                    parent = Comment.objects.get(id=parent_comment_id) if parent_comment_id else None

                    if 'file' in request.FILES:
                        file = request.FILES['file']
                    else:
                        file = None

                    comment = Comment(
                        file=file, text=text, email=email, user_name=user_name, home_page=home_page, 
                        parent_id=parent_comment_id, parent=parent
                    )
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
                    logger.error(f'Ошибка добавления комментария 77: {e}')
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Ошибка добавления комментария 80.',
                    })
            else:
                logger.error(f'Ошибка добавления комментария 83: {form.errors}')
                errors = []
                for field, messages in form.errors.items():
                    errors.extend(messages)
                return JsonResponse({
                    'status': 'error',
                    'message': f'Ошибка добавления комментария 86: {errors}',
                })

        return JsonResponse({
            'status': 'error',
            'message': 'Неверный запрос.',
        })


class CommentsView(View):
    template_name = 'comments/comments.html'
    COMMENTS_PER_PAGE = 25

    def get(self, request):

        sort_field = request.GET.get('sort', 'created_at')
        sort_direction = request.GET.get('direction', 'desc')
        page_number = request.GET.get('page', 1)

        allowed_fields = ["user_name", "email", "created_at"]
        allowed_order = ["asc", "desc"]

        if sort_field not in allowed_fields or sort_direction not in allowed_order:
            return JsonResponse({"error": "Invalid sort parameters"}, status=400)

        order_by = f"-{sort_field}" if sort_direction == "desc" else sort_field
        comments = Comment.objects.filter(parent_id=None).order_by(order_by)

        paginator = Paginator(comments, self.COMMENTS_PER_PAGE)
        page_obj = paginator.get_page(page_number)

        def build_tree(comment):
            return {
                "id": comment.id,
                "user_name": comment.user_name,
                "email": comment.email,
                "created_at": comment.created_at.strftime('%d-%m-%Y в %H:%M:%S'),
                "text": comment.text,
                "children": [build_tree(child) for child in comment.children.all().order_by(order_by)]
            }

        comment_tree = [build_tree(comment) for comment in page_obj]
            
        return render(request, self.template_name, {'comments': comment_tree, 'page_obj': page_obj})

    def form_valid(self, form):
            user_name = form.cleaned_data['user_name']
            email = form.cleaned_data['email']
            home_page = form.cleaned_data['home_page']
            captcha = form.cleaned_data['captcha']
            text = form.cleaned_data['text']

            CommentUtil.add_comment(user_name, email, home_page, captcha, text)
            return super().form_valid(form)

class GetCaptchaView(View):
    def get(self, request):
        captcha_util = CaptchaUtil()

        return captcha_util.get_captcha(request)
