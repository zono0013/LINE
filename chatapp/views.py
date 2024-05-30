from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View


# チャット画面を表示するビュー
class ChatView(View):
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        user = request.user
        return render(request,"chat.html",{"user":user})

chat   = ChatView.as_view()


# ログイン画面を表示するビュー
class LoginView(View):
        def get(self,request,*args,**kwargs):
            return render(request,"login.html")
    
        def post(self,request,*args,**kwargs):
            # ログイン時に表示するページとログイン機能
            if request.method == 'POST':
                username = request.POST.get('username')
                password = request.POST.get('password')

                # ユーザー認証
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    # ログイン成功
                    login(request, user)
                    return redirect('chat:chat_rooms')
                else:
                    # ログイン失敗
                    messages.error(request, 'ユーザー名またはパスワードが間違っています。')

            return render(request,"login.html")

loginview = LoginView.as_view()


# ユーザー作成画面を表示するビュー
class CreateLoginView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"create_login.html")

    def post(self,request,*args,**kwargs):
        if request.method == 'POST':
            new_username = request.POST.get('new_username')
            new_password = request.POST.get('new_password')
            try:
                # 新しいユーザーオブジェクトを作成し、ユーザー名とパスワードを設定
                user = User.objects.create_user(username=new_username, password=new_password)
            except Exception as e:
                # ユーザ作成失敗
                messages.error(request, 'ユーザーの作成に失敗しました。エラー: {}'.format(str(e)))

            # ログイン処理
            user = authenticate(request, username=new_username, password=new_password)
            if user is not None:
                # ログイン成功
                messages.error(request, 'ログインに成功しました。')
                login(request, user)
                return redirect('chat:chat_rooms')
            else:
                # ログイン失敗
                messages.error(request, 'ユーザー名またはパスワードが間違っています。ユーザー名: {}'.format(new_password))
        return render(request,"create_login.html")
    
create_login = CreateLoginView.as_view()