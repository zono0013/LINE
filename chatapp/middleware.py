from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class RedirectIfAuthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ユーザーが認証されており、ログインページにアクセスしようとしている場合
        if request.user.is_authenticated and request.path == reverse('chat:login'):
            return redirect('chat:chat_rooms')  # チャット画面にリダイレクト

        response = self.get_response(request)
        return response
