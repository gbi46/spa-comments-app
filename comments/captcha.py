class CaptchaUtil:
    def generate_captcha(request):
        # Генерация случайного текста для капчи (можно использовать буквы и цифры)
        captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        # Создание изображения капчи
        image = ImageCaptcha(width=160, height=60)
        
        # Генерация изображения с текстом капчи
        image_data = image.generate(captcha_text)

        # Преобразуем изображение в HTTP-ответ
        response = HttpResponse(image_data, content_type="image/png")
        
        # Сохраняем капчу в сессии для дальнейшей валидации
        request.session['captcha'] = captcha_text
        
        return response

    def check_captcha(request):
        user_captcha = request.POST.get('captcha')
        session_captcha = request.session.get('captcha')
        
        if user_captcha and user_captcha.lower() == session_captcha.lower():
            # Капча введена верно
            # Обрабатываем остальные данные формы
            return HttpResponse("Форма отправлена успешно!")
        else:
            # Неверная капча
            return HttpResponse("Неверный код с картинки. Попробуйте снова.")

    def get_image(image_bytes):
        pass