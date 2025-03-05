from .views import CommentsView, AddCommentView, get_captcha
from django.urls import path

app_name = 'comments'

urlpatterns = [
    path('', CommentsView.as_view(), name='comments_list'),
    path('add_comment/', AddCommentView.as_view(), name='add_comment'),
    path('captcha/', include('captcha.urls')),
    path('captcha/', get_captcha, name='get_captcha'),
]