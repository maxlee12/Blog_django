from django.shortcuts import render,render_to_response
from django.http import HttpResponse
import os

from .Itchat_ana import WXanalyse

# Create your views here.


def itchats(request):


    WXanalyse.main()

    # 路径
    # shutil.copy(os.getcwd() + '/' + 'QR.png', '/home/mysite/static/QR.png')
    # abspath =  os.path.abspath('.')
    # imaPath = os.path.join(abspath+'/ItchatLearn/Itchat_ana/QR.png')
    # print('---',imaPath)
    # imaPath = './ItchatLearn/Itchat_ana/QR.png'
    # return HttpResponse(image_data, mimetype="image/png")

    imaPath = 'ItchatLearn/img/QQ.png'

    return render_to_response('ItchatLearn/itchats.html', {'path':imaPath})


    # return render(request,'ItchatLearn/itchats.html', {'path':imaPath})