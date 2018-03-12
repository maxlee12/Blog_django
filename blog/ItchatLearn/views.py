from django.shortcuts import render,render_to_response
from django.http import HttpResponse
import os

from .Itchat_ana import WXanalyse

# Create your views here.


def itchats(request):

    WXanalyse.login()
    imaPath = 'ItchatLearn/img/QR.png'
    return render_to_response('ItchatLearn/itchats.html', {'path':imaPath})


def getFriend(request):

    friends = WXanalyse.getFriend()
    print(friends)
    return render_to_response('ItchatLearn/itchats.html', {'path':friends})