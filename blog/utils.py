# -*- coding: utf-8 -*-
__author__ = 'yubin.yang'
__date__ = '2020/9/17 13:33'

from functools import wraps
import json
import pymysql
import os
from django.core.mail import EmailMultiAlternatives
import jwt
from jwt import exceptions
from blog.logs import logger
import json
import datetime
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import status
from rest_framework.response import Response

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_blog.settings'

SECRET_KEY = "RedFlowerParty"
# 偷懒就不区分环境了
# 本地环境
#BASE_URL = "http://localhost:8000"

# 生产环境改成
BASE_URL = "http://119.45.63.52:9090"


class MysqlDataBase:
    def __init__(self, **kwargs):
        """
        :param kwargs:
        connect_flag ：连接是否成功的标识
        host，usrname，password，name 连接数据库的必备配置信息
        db: 数据库连接
        cursor: 游标，用来执行sql

        :return:
        """
        self.host = kwargs['host']
        self.username = kwargs['user']
        self.password = kwargs['password']
        self.db = kwargs['db']
        self.port = kwargs['port']
        try:
            self.db = pymysql.connect(host=self.host, user=self.username,
                                      password=self.password, db=self.db, port=self.port,
                                      charset='utf8')
            self.cursor = self.db.cursor()
        except Exception as e:

            raise Exception("connect to {} failed, the reason:{}".format(self.host, e))

    def get_index_dict(self, cursor):
        """
        获取数据库对应表中的字段名
        """
        index_dict = dict()
        index = 0
        for desc in cursor.description:
            index_dict[desc[0]] = index
            index = index + 1
        return index_dict

    def pd_read_sql(self, sql):
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            index_dict = self.get_index_dict(cursor=self.cursor)
            res = []
            for datai in data:
                resi = dict()
                for indexi in index_dict:
                    resi[indexi] = datai[index_dict[indexi]]
                res.append(resi)
            return res
        except Exception as e:
            raise Exception("pd execute {} failed. the reason {}".format(sql, e))

    def close_db(self):
        self.db.commit()
        self.cursor.close()
        self.db.close()


def get_request_body(f):
    @wraps(f)
    def base_function(request, *args, **kwargs):
        if request.content_type == 'application/json':
            # print(request.body.decode('utf-8'))
            # if
            if request.body.decode('utf-8'):
                data = json.loads(request.body.decode('utf-8'))
                request_params = data
                params = dict()
                for k in request_params.keys():
                    params[k] = request_params[k]
            else:
                params = dict()
            request.POST = params
        else:
            return JsonResponse({'RetCode': -1, 'Message': "The Request Headers content-type must be application/json"})

        return f(request, *args, **kwargs)

    return base_function


# jwt验证生成token

def create_token(user_id, email):
    salt = SECRET_KEY
    # 构造header
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    # 构造payload
    payload = {
        'user_id': user_id,  # 自定义用户ID
        'email': email,  # 自定义用户名
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)  # 超时时间
    }
    token = jwt.encode(payload=payload, key=salt, algorithm="HS256", headers=headers).decode('utf-8')

    return token


# jwt验证
def authenticate(token):
    # 校验步骤：
    # 1、切割
    # 2、解密第二段，并判断是否过期
    # 3、验证第三段合法性
    salt = SECRET_KEY
    try:
        # 从token中获取payload【不校验合法性】
        # unverified_payload = jwt.decode(token, None, False)
        payload = {}
        # 从token中获取payload【校验合法性】
        payload = jwt.decode(token, salt, True)
        # payload = json.loads(result)
    except exceptions.ExpiredSignatureError:
        logger.error({'code': 1003, 'error': "token已失效"})
    except jwt.DecodeError:
        logger.error({'code': 1003, 'error': "token认证失败"})
    except jwt.InvalidTokenError:
        logger.error({'code': 1003, 'error': "非法的token"})

    # 三种情况：
    # 1、抛出异常
    # 2、返回元组
    # 3、返回None
    logger.info("获取到的payload:{0},token:{1}".format(payload, token))
    return payload, token


def send_mail(subject, text_content, from_mail, to_mail, html_content):
    """

    :param:
     subject:邮箱主题
     text_content: 文本内容（当html_content无效会显示text_content)
     html_content:
     from_mail : 发送人
     to_mail: 收件人list

    :return:
    """
    msg = EmailMultiAlternatives(subject, text_content, from_mail, to_mail)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# 拼接播报的消息
def create_message(token):
    text_content = "感谢您注册小彬彬的博客，请点击如下链接进行激活\n{0}/blog/activate?token={1}，如果点击上面的链接无效，" \
                   "请尝试将链接复制到浏览器地址栏访问。如果此链接已过期，请重发激活邮件.请勿回复此邮件…".format(BASE_URL, token)
    html_content = '<p>感谢您注册<a href="http://blog.yybgzh.cn/" target=blank>小彬彬的博客</a><p>' \
                   '<p>请点击如下链接进行激活<p>' \
                   '<p>{0}/blog/activate?token={1}<p>' \
                   '<p>如果点击上面的链接无效，请尝试将链接复制到浏览器地址栏访问。</p>' \
                   '<p>如果此链接已过期，请重发激活邮件</p>' \
                   '<p style="color:red">请勿回复此邮件…</p>'.format(BASE_URL, token)
    return text_content, html_content


# 处理comment消息格式的方法
def get_comment_id(my_list, parent_id, my_dict):
    for nlist in my_list:
        if nlist.get('comment_id') == parent_id:
            nlist.get('ChildsSon').append(my_dict)
        else:
            if nlist.get('ChildsSon'):
                # 递归
                get_comment_id(nlist.get('ChildsSon'), parent_id, my_dict)
            else:
                continue


# 根据mylist中的comment_id获取index,然后获取后面5条记录。。
def get_list_index(ll, comment_id):
    for n in range(0, len(ll)):
        if ll[n].get('comment_id') == int(comment_id):
            return n


# if __name__ == '__main__':
#     from_mail = 'yangyubin1@126.com(小彬彬的博客)'
#     to_mail = ['342785426@qq.com']
#     text_content = "感谢您注册小彬彬的博客，请点击如下链接进行激活，如果点击下面的链接无效，请尝试将链接复制到浏览器地址栏访问。如果此链接已过期，请重发激活邮件.请勿回复此邮件…"
#     html_content = '<p>感谢您注册<a href="http://http://blog.yybgzh.cn/" target=blank>小彬彬的博客</a><p>' \
#                    '<p>请点击如下链接进行激活<p>' \
#                    '<p>如果点击下面的链接无效，请尝试将链接复制到浏览器地址栏访问。</p>' \
#                    '<p>如果此链接已过期，请重发激活邮件</p>' \
#                    '<p style="color:red">请勿回复此邮件…</p>'
#     # 链接token用jwt方法生成
#
#     send_mail(subject='测试邮件', text_content=text_content, html_content=html_content, from_mail=from_mail,
#               to_mail=to_mail)



# django分页
def api_paging(objs, request, Serializer):
    """
    objs : 实体对象
    request : 请求对象
    Serializer : 对应实体对象的序列化
    """
    try:
        size = int(request.GET.get('size', 3))
        page = int(request.GET.get('page', 1))
    except (TypeError, ValueError):
        return Response({'code': 20001, "data": [], "msg": "page and size must be integer!"},
                        status=status.HTTP_400_BAD_REQUEST)
    paginator = Paginator(objs, size)  # paginator对象
    total = paginator.num_pages  # 总页数
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)

    serializer = Serializer(objs, many=True)  # 序列化操作

    return Response({'code': 20000, "data": serializer.data, "msg": "查询成功", 'total_page': total, 'page': page},
                    status=status.HTTP_200_OK)
