from django.shortcuts import render

# Create your views here.
import json
from django.http import HttpResponse
from .models import class_Android_user

def Analysis(Appneeds):
    case_num = Appneeds[0:4]
    message = Appneeds[4:-1]
    max_len = len(message)

    s_location = 0
    e_location = 0
    s_message = []
    while e_location < max_len:
        if (message[e_location] == ':'):
            s_message.append(message[s_location + 1:e_location])
            s_location = e_location
        e_location += 1
    s_message.pop(0)
    s_message.append(message[s_location+1:e_location])
    return [case_num, s_message]

def App_reg_2001(request,message):
    user_exsit = class_Android_user.objects.filter(user_name = message[0])
    print(type(user_exsit),len(user_exsit))
    print(user_exsit)
    if user_exsit.count() != 0:     #不为0表示有用户占用这个名字，不可以使用该用户名
        response_result = {"result":"user name occupied"}
        print("I am in")
        return json.dumps(response_result, ensure_ascii=False)
    print("I am not in")
    user_ip = ''
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
        user_ip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:  
        user_ip = request.META['REMOTE_ADDR']
    
    try:
        class_Android_user.objects.create(user_name = message[0],user_password = message[1],user_IP = user_ip,user_friends = '',user_groups = '',user_message_cache = '')
        response_result = {"result":"succeed"}
        return json.dumps(response_result, ensure_ascii=False)
    except:
        response_result = {"result":"failed"}
        return json.dumps(response_result, ensure_ascii=False)
        



def Android_needs_response(request,Appneeds):
    func_dic = {'2001':App_reg_2001,
           '2002':App_sign_in_2002,
           '2003':App_send_friends_2003,
           '2004':App_send_group_2004,
           '2005':App_get_group_2005,
           '2006':App_set_group_2006,
           }
    result = Analysis(Appneeds)
    case_num = result[0]
    message = result[1]
    print(result[0],result[1])
    func = func_dic[case_num]   #查询字典用[ ]，不是()
    App_json = func(request,message)
    print(App_json)
    return HttpResponse(App_json,content_type="application/json")
