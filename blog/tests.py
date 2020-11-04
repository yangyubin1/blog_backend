# # -*- coding: utf-8 -*-
# __author__ = 'yubin.yang'
# __date__ = '2020/8/28 15:49'
#
# ###jwt用法
# import jwt
# import datetime
# from jwt import exceptions
#
# SECRET_KEY = "RedFlowerParty"
#
#
# def create_token():
#     salt = SECRET_KEY
#     # 构造header
#     headers = {
#         'typ': 'jwt',
#         'alg': 'HS256'
#     }
#     # 构造payload
#     payload = {
#         'user_id': '2020091715340246',  # 自定义用户ID
#         'email': 'yy1b@123',  # 自定义用户名
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)  # 超时时间
#     }
#     token = jwt.encode(payload=payload, key=salt, algorithm="HS256", headers=headers).decode('utf-8')
#
#     return token
#
#
# class JwtQueryParamsAuthentication():
#     def authenticate(self, token):
#         # 校验步骤：
#         # 1、切割
#         # 2、解密第二段，并判断是否过期
#         # 3、验证第三段合法性
#         salt = SECRET_KEY
#         try:
#             # 从token中获取payload【不校验合法性】
#             # unverified_payload = jwt.decode(token, None, False)
#
#             # 从token中获取payload【校验合法性】
#             payload = jwt.decode(token, salt, True)
#         except exceptions.ExpiredSignatureError:
#             print({'code': 1003, 'error': "token已失效"})
#         except jwt.DecodeError:
#             print({'code': 1003, 'error': "token认证失败"})
#         except jwt.InvalidTokenError:
#             print({'code': 1003, 'error': "非法的token"})
#
#         # 三种情况：
#         # 1、抛出异常
#         # 2、返回元组
#         # 3、返回None
#         print(payload, token)
#         return (payload, token)
#
#
# # print(create_token())
# # eyJhbGciOiJIUzI1NiIsInR5cCI6Imp3dCJ9.eyJleHAiOjE2MDAzMzk5OTksImVtYWlsIjoieXkxYkAxMjMiLCJ1c2VyX2lkIjoiMjAyMDA5MTcxNTM0MDI0NiJ9.bMQHjkiYvxJqxpfVkUSsYJGiQScuK5-bFz9AY_fn1Is
# if __name__ == '__main__':
#     token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6Imp3dCJ9.eyJlbWFpbCI6IjM0Mjc4NTQyNkBxcS5jb20iLCJ1c2VyX2lkIjoiMjAyMDA5MTgxNzE0MzU2NiIsImV4cCI6MTYwMDQyNDA3Nn0.kzR5-tKqq8PcmKZkroufbqZYDN1swkETnumxVcpCJt0'
#     my_jwt = JwtQueryParamsAuthentication()
#     my_jwt.authenticate(token)

# data = {'is_notice': 'Y'}
# print(**data)

def get_comment_id(my_list, parent_id, my_dict):
    for nlist in my_list:
        if nlist.get('comment_id') == parent_id:
            nlist.get('ChildsSon').append(nlist)
        else:
            if nlist.get('ChildsSon'):
                # 递归
                get_comment_id(nlist.get('ChildsSon'), parent_id, my_dict)
            else:
                continue


result_list = [{'user_id': '123', 'label': '小呆萌', 'id': 1, 'username': 'binbin', 'content': '啊呀呀1', 'article_id': 5,
                'time': '2020-09-25 14:48:09', 'parent_comment_id': 0, 'avatar': 'boy.png'},
               {'user_id': '123', 'label': '小呆萌', 'id': 2, 'username': 'binbin', 'content': '啊呀呀2', 'article_id': 5,
                'time': '2020-09-25 14:47:59', 'parent_comment_id': 0, 'avatar': 'boy.png'},
               {'user_id': '123', 'label': '小呆萌', 'id': 3, 'username': 'binbin', 'content': '啊呀呀3', 'article_id': 5,
                'time': '2020-09-25 15:02:26', 'parent_comment_id': 2, 'avatar': 'boy.png'},
               {'user_id': '123', 'label': '萌萌哒', 'id': 4, 'username': 'haha', 'content': '啊呀呀4', 'article_id': 5,
                'time': '2020-09-25 15:02:47', 'parent_comment_id': 3, 'avatar': 'girl.png'},
               {'user_id': '2020092214073579', 'label': '小萌新', 'id': 5, 'username': '342785426', 'content': '1[微笑]',
                'article_id': 5, 'time': '2020-09-25 15:56:59', 'parent_comment_id': 0, 'avatar': 'boy.png'},
               {'user_id': '2020092214073579', 'label': '小萌新', 'id': 6, 'username': '342785426', 'content': '2[微笑]',
                'article_id': 5, 'time': '2020-09-25 15:57:39', 'parent_comment_id': 0, 'avatar': 'boy.png'},
               {'user_id': '2020092214073579', 'label': '小萌新', 'id': 7, 'username': '342785426', 'content': '123',
                'article_id': 5, 'time': '2020-09-25 16:01:41', 'parent_comment_id': 0, 'avatar': 'boy.png'},
               {'user_id': '2020092214073579', 'label': '小萌新', 'id': 8, 'username': '342785426', 'content': '123',
                'article_id': 5, 'time': '2020-09-25 16:01:59', 'parent_comment_id': 0, 'avatar': 'boy.png'},
               {'user_id': '2020092214073579', 'label': '小萌新', 'id': 9, 'username': '342785426', 'content': '12',
                'article_id': 5, 'time': '2020-09-25 16:06:54', 'parent_comment_id': 0, 'avatar': 'boy.png'},
               {'user_id': '2020092214073579', 'label': '小萌新', 'id': 10, 'username': '342785426', 'content': '123',
                'article_id': 5, 'time': '2020-09-25 16:07:17', 'parent_comment_id': 0, 'avatar': 'boy.png'},
               {'user_id': '2020092214073579', 'label': '小萌新', 'id': 11, 'username': '342785426', 'content': '124',
                'article_id': 5, 'time': '2020-09-25 16:08:16', 'parent_comment_id': 0, 'avatar': 'boy.png'},
               {'user_id': '2020092214073579', 'label': '小萌新', 'id': 12, 'username': '342785426', 'content': '123',
                'article_id': 5, 'time': '2020-09-25 16:08:52', 'parent_comment_id': 0, 'avatar': 'boy.png'}]

# 循环，只处理pid为0的数据，如果碰到>0的就不处理，超过5条就退出（假设分页为5）
for n in range(0, len(result_list)):
    count = 0  # 记录list量
    Result_List = []
    myDict = {'comment_id': result_list[n].get('id'), 'avatar': result_list[n].get('avatar'),
              'username': result_list[n].get('username'), 'label': result_list[n].get('label'),
              'time': result_list[n].get('time'), 'content': result_list[n].get('content'), 'ChildsSon': []}
    # 等于0则记录
    if result_list[n].get('parent_comment_id') == 0:
        result_list.append(myDict)
    else:
        # 如果父节点非0，即有父节点的话，就要添加在父节点字典中的childson的list里面
        get_comment_id(result_list, result_list[n].get('parent_comment_id'), myDict)
    if len(result_list)>=5:
        break
# aaa = [
#     {"comment_id": "1", "avatar": "boy.png", "username": "123", "label": "小呆萌", "time": "2020-09-28", "content": "123",
#      "ChildsSon": [{"comment_id": "2", "avatar": "boy.png", "username": "123", "label": "小呆萌", "time": "2020-09-28",
#                     "content": "123",
#                     "ChildsSon": [
#                         {"comment_id": "3", "avatar": "boy.png", "username": "123", "label": "小呆萌",
#                          "time": "2020-09-28",
#                          "content": "123",
#                          "ChildsSon": []},
#                         {"comment_id": "4", "avatar": "boy.png", "username": "123", "label": "小呆萌",
#                          "time": "2020-09-28",
#                          "content": "123",
#                          "ChildsSon": []}]}]},
#     {"comment_id": "5", "avatar": "boy.png", "username": "123", "label": "小呆萌", "time": "2020-09-28", "content": "123",
#      "ChildsSon": []}]
#
# ddd = {"comment_id": "6", "avatar": "boy.png", "username": "123", "label": "小呆萌", "time": "2020-09-28",
#        "content": "123",
#        "ChildsSon": []}
#
# print("old:", aaa)
# get_comment_id(aaa, "5", ddd)
# print("new:", aaa)
