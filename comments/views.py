from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Comment

class CommentsView(View):
    template_name = 'comments/comments.html'

    def get(self, request):

        comments = Comment.objects.all()
        return render(request, self.template_name, {'comments': comments})


from .models import Comment

class AddCommentView(CreateView):
    model = Comment
    template_name = 'comments/add_comment.html'
    fields = ['user_name', 'email', 'home_page', 'captcha', 'text']
    success_url = reverse_lazy('comments:comments_list')

