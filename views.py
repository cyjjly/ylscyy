from lib._init_ import JR

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password

import json,traceback
from main.models import User

class SignHandler:
    def handle(self,request):
        pd =json.loads(request.body)


        action=pd.get('action')

        request.pd=pd

        if action =='signin':
            return self.signin(request)
        elif action =='signout':
            return self.signout(request)
        else:
            return JR({'ret': 2, 'msg': 'action参数错误'})


    def signin(self,request):

        userName = self.pd.get("username")
        passWord = self.pd.get('password')

        # 使用 Django auth 库里面的 方法校验用户名、密码
        user = authenticate(username=userName, password=passWord)

        # 如果能找到用户，并且密码正确
        if user is None:
            return JR({'ret': 1, 'msg': '用户名或者密码错误'})

        if not user.is_active:
            return JR({'ret': 0, 'msg': '用户已经被禁用'})

        login(request, user)

        return JR(
            {
                "ret":0,
                "usertype":user.usertype,
                "userid":user.id,
                "realname":user.realname
            }
        )



    def signout(self,request):
        #使用登出方法
        logout(request)
        return JR({'ret': 0})



class AccountHandler:
    def handle(self,request):
        if request.method=='GET':
            pd=request.GET
        else:
            pd =json.loads(request.body)

        request.pd = pd

        action=pd.get('action')


        if action =='listbypage':
            return self.listbypage(request)
        elif action =='addone':
            return self.addone(request)
        elif action =='modifyone':
            return self.modifyone(request)
        elif action =='deleteone':
            return self.deleteone(request)
        else:
            return JR({'ret': 2, 'msg': 'action参数错误'})

    def addone(self,request):

        data=request.pd.get('data')

        ret=User.addone(data)

        return JR(ret)


    def listbypage(self,request):

        pagenum=int(request.pd.get('pagenum'))
        pagesize = int(request.pd.get('pagesize'))
        keywords = request.pd.get('keywords')
        ret=User.listbypage(pagenum,pagesize,keywords)

        return JR(ret)
