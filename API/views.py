from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
import datetime
from . import functionsRasp
import json

from django.conf import settings
from django.core.mail import send_mail

def getRasp(request):
    try:
        dataType = request.GET['dataType']
        if dataType == 'json':
            try:
                searchName = request.GET['searchName']
                date_time_str = request.GET['dateNum']
                date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
                URL = functionsRasp.funcRasp.urlRasp(date_time_obj.date())
                raspList = functionsRasp.funcRasp.resRasp(URL, searchName, True)
                jSUN = functionsRasp.funcRasp.parsRasp(raspList)
                if raspList:
                    return HttpResponse(json.dumps({'response': jSUN}, ensure_ascii=False), content_type="application/json")
                else:
                    return HttpResponse(False)
            except MultiValueDictKeyError:
                jSUN = {
                    'code': 500,
                    'mesg': 'error'
                }
                return HttpResponse(json.dumps({'response': jSUN}, ensure_ascii=False), content_type="application/json")
        elif dataType == 'photo':
            try:
                searchName = request.GET['searchName']
                date_time_str = request.GET['dateNum']
                date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
                URL = functionsRasp.funcRasp.urlRasp(date_time_obj.date())
                if URL != '#norasp':
                    raspList = functionsRasp.funcRasp.resRasp(URL, searchName)
                    if raspList:
                        time = ['8:30-10:00', '10:20-11:50', '12:25-13:55', '14:05-15:35', '15:45-17:00']
                        context = {
                            'date': f'{date_time_obj.date().day} {functionsRasp.mnths[date_time_obj.date().month][0]} {date_time_obj.date().year}г',
                            'searchName': searchName,
                            'raspList': raspList,
                            'time': time,
                        }
                        return render(request, 'API/index.html', context)
                    else:
                        return HttpResponse(123)
                else:
                    jSUN = {
                        'code': 403,
                        'mesg': 'norasp'
                    }
                    return HttpResponse(json.dumps({'response': jSUN}, ensure_ascii=False), content_type="application/json")
            except MultiValueDictKeyError:
                jSUN = {
                    'code': 500,
                    'mesg': 'error'
                }
                return HttpResponse(json.dumps({'response': jSUN}, ensure_ascii=False), content_type="application/json")
        else:
            jSUN = {
                'code': 400,
                'mesg': 'error'
            }
            return HttpResponse(json.dumps({'response': jSUN}, ensure_ascii=False), content_type="application/json")
    except:
        jSUN = {
            'code': 400,
            'mesg': 'request error'
        }
        return HttpResponse(json.dumps({'response': jSUN}, ensure_ascii=False), content_type="application/json")

# api/?searchName=ИСиП-42&dateNum=2023-02-22&dataType=photo