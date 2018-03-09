from django.shortcuts import render,render_to_response
from django.http import HttpResponse
import os
# Create your views here.


def itchats(request):

    abspath =  os.path.abspath('.')
    imaPath = os.path.join(abspath+'/ItchatLearn/Itchat_ana/QR.png')
    print('---',imaPath)
    imaPath = './ItchatLearn/Itchat_ana/QR.png'

    image_data = open(imaPath, "rb").read()
    # return HttpResponse(image_data, mimetype="image/png")

    return render_to_response('lawBlog/itchats.html', {'path':imaPath})


