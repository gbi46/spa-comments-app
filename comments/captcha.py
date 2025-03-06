from captcha.image import ImageCaptcha
from django.http import HttpResponse, JsonResponse
import base64
import random, string

class CaptchaUtil:
    def generate_captcha(self, request):
        # Генерация случайного текста для капчи (можно использовать буквы и цифры)
        captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        # Создание изображения капчи
        image = ImageCaptcha(width=160, height=60)
        
        # Генерация байтов капчи
        image_bytes = image.generate(captcha_text).read()
        
        # Сохраняем капчу в сессии для дальнейшей валидации
        request.session['captcha'] = captcha_text
        
        return captcha_text, image_bytes

    def check_captcha(request):
        user_captcha = request.POST.get('captcha')
        session_captcha = request.session.get('captcha')
        
        if user_captcha and user_captcha.lower() == session_captcha.lower():
            return True
        else:
            return False

    def get_image(self, image_bytes):
        return base64.b64encode(image_bytes).decode('utf-8')

    def get_captcha(self, request):
        captcha_text, image_bytes = self.generate_captcha(request)
        captcha_image = self.get_image(image_bytes)

        return JsonResponse({
            'captcha_text': captcha_text, 
            'captcha_image': f"data:image/png;base64,{captcha_image}"
        })