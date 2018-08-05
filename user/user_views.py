from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect

from user.forms import RegisterForm
from user.models import User


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.save()
            # 设置用户登录状
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            request.session['icon'] = user.icon
            return redirect('/user/info/')
        else:
            return render(request, "register.html", {"error": form.errors})

    return render(request, 'register.html')


def login(request):
    if request.method == "POST":
        nickname = request.POST.get("nickname")
        password = request.POST.get("password")
        user = User.objects.filter(nickname=nickname)

        if user.exists():
            user = user[0]
            if check_password(password, user.password):
                request.session["uid"] = user.id
                request.session['nickname'] = user.nickname
                return redirect('/user/info/')
            else:
                return render(request, 'login.html', {"error": "用户名或密码错误"})
        else:
            return render(request, 'login.html', {"error": "用户名或密码错误"})

    else:
        return render(request, 'login.html')


def logout(request):
    request.session.flush()
    # request.cookies.flush()
    return render(request, 'login.html')


def user_info(request):
    uid = request.session.get('uid')
    user = User.objects.get(id=uid)
    print(user)
    return render(request, 'user_info.html', {"user": user})
