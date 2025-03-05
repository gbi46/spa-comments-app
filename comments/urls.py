from .views import CommentsView, AddCommentView
from django.urls import path

app_name = 'comments'

urlpatterns = [
    path('', CommentsView.as_view(), name='comments_list'),
    path('add_comment/', AddCommentView.as_view(), name='add_comment'),
]