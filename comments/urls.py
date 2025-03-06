from .captcha import CaptchaUtil
from .views import AddCommentView, CommentsView, GetCaptchaView 
from .utils import CommentUtil
from django.urls import path

app_name = 'comments'

urlpatterns = [
    path('', CommentsView.as_view(), name='comments_list'),
    path('add_comment/', AddCommentView.as_view(), name='add_comment'),
    path('captcha/', GetCaptchaView.as_view(), name='get_captcha'),
]