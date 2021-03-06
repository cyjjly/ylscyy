from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password

from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage

import traceback

# 可以通过 命令 python  manage.py createsuperuser 来创建超级管理员
# 就是在这User表中添加记录
class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)

    # 用户类型
    # 1： 超管 | 1000： 普通管理员  | 2000：学生  |  3000： 老师
    usertype = models.PositiveIntegerField()

    # 真实姓名
    realname = models.CharField(max_length=30, db_index=True)

    # 学号
    studentno = models.CharField(
        max_length=10,
        db_index=True,
        null=True, blank=True
    )

    # 备注描述
    desc = models.CharField(max_length=500, null=True, blank=True)

    REQUIRED_FIELDS = ['usertype', 'realname']

    class Meta:
        db_table = "cimp_user"

    @staticmethod
    def listbypage(pagenum,pagesize,keywords):

        try:
            qs = User.objects.values('id','username','realname','studentno','desc','usertype')\
                .order_by('-id')

            if keywords:
                conditions = [Q(realname__contains=one) for one in keywords.split(' ') if one]
                query = Q()
                for condition in conditions:
                    query &= condition
                qs = qs.filter(query)



            # 使用分页对象，设定每页多少条记录
            pgnt = Paginator(qs, pagesize)

            # 从数据库中读取数据，指定读取其中第几页
            page = pgnt.page(pagenum)

            # 将 QuerySet 对象 转化为 list 类型
            retlist = list(page)

            # total指定了 一共有多少数据
            return {'ret': 0, 'items': retlist, 'total': pgnt.count,'keywords':keywords}

        except EmptyPage:
            return {'ret':0,'items':[],'total':0,'keywords':keywords}

        except:
            err = traceback.format_exc()
            return {'ret': 2, 'msg': err}
