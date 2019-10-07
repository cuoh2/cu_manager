import os
from datetime import datetime

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render

# Create your views here.
from cu_manager import settings
from manager.views import login_required
from remoteCMD.models import CmdList
from remoteCMD.remote import Remote, SFtp

showFlag = ''

@login_required
def remote_cmd(request):
    username=request.COOKIES.get('name', '')
    if request.method == 'POST' and request.POST:
        if 'sendcmd' in request.POST:
            ip=request.POST['ip']
            user=request.POST['username']
            password=request.POST['password']
            cmd=request.POST['cmd']
            port=int(request.POST['port']) or 22

            db_cmd=CmdList()
            db_cmd.host=ip
            db_cmd.cmd=cmd
            time=datetime.now()
            db_cmd.time=time
            db_cmd.save()

            handler=Remote(host=ip, username=user, password=password, port=port)
            remote=handler.ssh(cmd)
            showFlag='remote'
            return render(request, 'remote_cmd.html', locals())

        elif 'history' in request.POST:
            cmds=CmdList.objects.order_by('-id')[:6]
            results=[]
            for item in cmds:
                results.append({
                    'time': item.time.strftime('%m-%d %H:%M:%S'),
                    'cmd': item.cmd,
                    'host': item.host,
                })
            showFlag='result'
            return render(request, 'remote_cmd.html', locals())

    return render(request, 'remote_cmd.html')


@login_required
def file_trans(request):
    """文件传输"""
    username=request.COOKIES.get('name', '')
    if request.method == 'POST' and request.POST:
        if 'upload' in request.POST:
            if 'upload_file' in request.FILES:
                file=request.FILES.get('upload_file', '')
                save_path=default_storage.save('../eru_manager/upload/' + file.name, ContentFile(file.read()))
                tmp_file=os.path.join(settings.BASE_DIR, save_path)
                is_success=True
                upload_tips='上传成功'
                return render(request, 'file_trans.html', locals())
            else:
                is_success=False
                upload_tips='上传失败'
                return render(request, 'file_trans.html', locals())
        elif 'put_file' in request.POST:  # 文件分发
            des_ip=request.POST['des_ip']
            client_user=request.POST['client_user']
            client_passwd=request.POST['client_passwd']
            put_file_path=request.POST['put_file_path']
            save_path=request.POST['save_path']

            sftp=SFtp(host=des_ip, username=client_user, password=client_passwd)

            try:
                if save_path:
                    sftp.put(put_file_path, save_path)
                else:
                    sftp.put(put_file_path)
                is_put=True
                put_tips='发送成功'
                return render(request, 'file_trans.html', locals())
            except Exception as e:
                print(e)
                is_put=False
                put_tips='发送失败'
                return render(request, 'file_trans.html', locals())
        else:
            return render(request, 'file_trans.html', locals())
    return render(request, 'file_trans.html', locals())

