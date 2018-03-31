from django.shortcuts import render,render_to_response
from django.http import HttpResponse
import os
import itchat
from .Itchat_ana import WXanalyse

# Create your views here.



def logInSuccess():
    print('登录成功')
    pass

def logInExit():
    print('已经登出')
    pass

def showQR():
    print('获得二维码')
    imaPath = 'ItchatLearn/img/QR.png'
    return render_to_response('ItchatLearn/itchats.html', {'path':imaPath})
    pass


def itchats(request):
    def qrCallback(uuid,status,qrcode):
        print('qrCallback')
        pass

    pwd = os.getcwd() + '/ItchatLearn/static/ItchatLearn/img/QR.png'
    uuid = itchat.get_QRuuid()
    print(uuid)
    qr = itchat.get_QR(uuid=uuid,qrCallback=qrCallback, picDir=pwd)
    print(qr)

    if qr:
        imaPath = 'ItchatLearn/img/QR.png'
        return render_to_response('ItchatLearn/itchats.html', {'path': imaPath ,'msg':''})
    else:
        return render_to_response('ItchatLearn/itchats.html', {'path': '' ,'msg': '消息'})





