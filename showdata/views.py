from django.http import JsonResponse
from django.shortcuts import render

from manager.views import login_required
from showdata.models import CPUData



def save_data(request):
    result = {'status': 'error', 'err_msg': ''}
    if request.method == 'POST' and request.POST:
        data = request.POST['data']
        time = request.POST['time']
        cpu = CPUData()
        cpu.data = data
        cpu.time = time
        cpu.save()

        result['status']='success'
        result['err_msg']=0
        result['time']=time
    else:
        result['err_msg']='请求方法必须为 POST, 不能为空'
    return JsonResponse(result)

def get_data(request):
    data = CPUData.objects.order_by('-id')[0]
    time = data.time
    result = {
        'time': time.strftime('%H:%M:%S'),
        'data': data.data
    }
    return JsonResponse(result)


@login_required
def show_data(request):
    user_name = request.COOKIES.get('name')
    return render(request,'show_data.html',locals())