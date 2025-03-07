from .captcha import CaptchaUtil
from .views import AddCommentView, CommentsView, GetCaptchaView 
from .utils import CommentUtil
from django.urls import path
from django.conf.urls import handler404

app_name = 'comments'

urlpatterns = [
    path('', CommentsView.as_view(), name='comments_list'),
    path('add_comment/', AddCommentView.as_view(), name='add_comment'),
    path('captcha/', GetCaptchaView.as_view(), name='get_captcha'),
]

def custom_404_view(request, exception):
    return render(request, "404.html", status=404)

handler404 = custom_404_view