class JWTAuthenticationFromCookiesMiddleware:
    """
    Middleware для извлечения JWT-токена из cookies и установки его в заголовок Authorization.

    Этот класс middleware автоматически извлекает `access_token` из cookies входящего HTTP-запроса
    и устанавливает его в заголовок `Authorization` в формате `Bearer <token>`. Это позволяет
    использовать существующие механизмы аутентификации, которые ожидают токен в заголовке,
    даже если токен хранится в cookies.

    Использование данного middleware особенно полезно в случаях, когда фронтенд сохраняет токены
    в httpOnly cookies для повышения безопасности и предотвращения доступа к токенам через JavaScript.
    """
    def __init__(self, get_response):
        """
        Инициализирует middleware.

        :param get_response: Функция для получения ответа на запрос.
        :type get_response: callable
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Обрабатывает входящий HTTP-запрос.

        Извлекает `access_token` из cookies и устанавливает его в заголовок `Authorization`,
        если токен присутствует.

        :param request: Входящий HTTP-запрос.
        :type request: django.http.HttpRequest
        :return: Ответ на запрос.
        :rtype: django.http.HttpResponse
        """
        # Извлекаем токены из cookies
        access_token = request.COOKIES.get('access_token')
        if access_token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

        response = self.get_response(request)
        return response
