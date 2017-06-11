# -*- coding: utf-8 -*-
 
from django.http import HttpResponse
from django.shortcuts import render_to_response

from . import updateWebSource,updateLogin
import json


def main(request):
    '''request for updateWebSource '''
    webSourceInfo = []   
    dbSourceInfo = [] 
    webSourceInfo.append(updateWebSource.classReadWebSouce().getInfo())  
    dbSourceInfo.append(updateLogin.readConn().getInfo()) 
    return render_to_response('GURU/main.html',{
        'webSourceInfo':json.dumps(webSourceInfo),
        'dbSourceInfo':json.dumps(dbSourceInfo)
    })