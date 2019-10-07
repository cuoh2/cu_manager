from django.shortcuts import render, redirect, reverse

# Create your views here.m

from manager.models import UserInfo, HostInfo
from remoteCMD.remote import get_host_info


def register(request):
    if request.method == 'POST' and request.POST:
        username=request.POST['name']
        if UserInfo.objects.filter(name=username):
            warn='用户名已经存在, 请重新输入'
            return render(request, 'register.html', locals())
        else:
            user=UserInfo()
            user.name=username
            password=request.POST['password']
            email=request.POST['email']
            user.password = UserInfo.hash_password(password)
            user.email=email
            user.save()
            response=redirect(reverse('hostlist'))
            response.set_cookie('name', username, max_age=3600 * 12)
            request.session['name']=username
            return response
            #return redirect(reverse('login'))
    else:
        return render(request, 'register.html')



def login(request):
    if request.method == 'POST' and request.POST:
        username = request.POST['name']
        password = request.POST['password']
        password = UserInfo.hash_password(password)
        if UserInfo.objects.filter(name=username,password=password):
            response=redirect(reverse('index'))
            response.set_cookie('name', username, max_age=3600 * 12)
            request.session['name']=username
            return response
        else:
            error = '用户名或者密码错误, 请重新输入'
            return render(request, 'login.html', locals())
    else:
        return render(request, 'login.html', locals())


def logout(request):
    request.session.clear()
    response = redirect(reverse('index'))
    response.delete_cookie('name')
    return response


def login_required(func):
    def wrapper(request,*args,**kwargs):
        if not request.COOKIES.get('name'):
            return redirect(reverse('login'))
        return func(request,*args,**kwargs)
    return wrapper

@login_required
def index(request):
    username=request.COOKIES.get('name', '')
    return render(request, 'index.html', locals())

@login_required
def hostlist(request):
    username = request.COOKIES.get('name', '')
    hostlist = HostInfo.objects.filter(is_delete=False)
    return render(request, 'hostlist.html', locals())

@login_required
def add_host(request):
    username=request.COOKIES.get('name', '')
    if request.method == 'POST' and request.POST:
        host_ip=request.POST['ip']
        if host_ip == '' or HostInfo.objects.filter(ip=host_ip,is_delete=False):
            error = '该ip已存在，请重新输入'
            return render(request, 'add_host.html', locals())
        nickname=request.POST['nickname']
        password=request.POST['password']
        admin=request.POST['admin']
        if get_host_info(host_ip, admin, password, nickname):
            is_add=0
            return render(request, 'add_host.html', locals())
        else:
            is_add=1
            return render(request, 'add_host.html', locals())
    return render(request, 'add_host.html', locals())


@login_required
def del_host(request):
    id=request.GET.get('id')
    host=HostInfo.objects.get(id=id)
    host.is_delete=True
    host.save()
    return redirect(reverse('hostlist'))

