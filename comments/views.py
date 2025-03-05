from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Comment
from .utils import CommentSerializer, CommentUtil

from django.urls import reverse
from django.views.generic.edit import CreateView
from .models import Comment
from .forms import CommentForm
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class AddCommentView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save()

            comment.user = request.user
            comment.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    captcha_text, image_bytes = CommentUtil.generate_captcha()
    request.session['captcha_text'] = captcha_text
    captcha_image = f"data:image/png;base64,{image_bytes.decode('latin1')}"
    return JsonResponse({'image': captcha_image})

