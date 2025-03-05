from PIL import Image, ImageDraw, ImageFont
from rest_framework import serializers
from .models import Comment

class CommentUtil:
    def generate_captcha():

        captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        # Создание изображения капчи
        image = Image.new('RGB', (120, 40), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        draw.text((10, 10), captcha_text, font=font, fill=(0, 0, 0))

        # Преобразование изображения в байты
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        image_bytes = buffer.getvalue()

        return captcha_text, image_bytes

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
