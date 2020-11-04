# from rest_framework.decorators import detail_route
# -*- coding: utf-8 -*-
import os
import datetime
import random
from django.db.models import F
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import RecipeSerializer, BlogArticleSerializer, BlogArticlePlatformSerializer, \
    BlogNavMenuListSerializer, BlogFriendsSerializer, BlogAboutMeSerializer, BlogUserSerializer, \
    BlogCollectLikeSerializer, BlogGuestLogSerializer
from .models import Recipe, BlogArticle, BlogArticlePlatform, BlogNavMenuList, BlogFriends, BlogAboutMe, BlogUserInfo, \
    BlogCollectLikeInfo, ArticleComment, BlogGuestLog, BlogLikeNum
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.http import Http404
from test_blog.settings import MEDIA_ROOT, DATABASE_SC_URL, PAGE_SIZE
from blog.logs import logger
from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import redirect
from blog.utils import get_request_body
from apscheduler.schedulers.background import BackgroundScheduler
from blog.utils import send_mail, create_token, create_message, authenticate, get_comment_id, get_list_index, \
    api_paging, MysqlDataBase


def writeFile(filePath, file):
    with open(filePath, "wb") as f:
        if file.multiple_chunks():
            for content in file.chunks():
                f.write(content)
        else:
            data = file.read()  ###.decode('utf-8')
            f.write(data)


#
#
class MyPageNumber(PageNumberPagination):
    page_size = 3  # 每页显示多少条
    page_size_query_param = 'size'  # URL中每页显示条数的参数
    page_query_param = 'page'  # URL中页码的参数
    max_page_size = 100  # 最大页码数限制


# restframework views主要抒写办法https://www.jianshu.com/p/3cec36add17d


class TestView(APIView):
    def get(self, request):
        return Response({'data': "hello,world"})


# Create your views here.

class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()


class BlogArticleViewSet(APIView):
    def get(self, request, format=None):
        article_list = BlogArticle.objects.all().order_by("-create_time")  # 分页查询，查询所有

        # page_obj = MyPageNumber()
        # page_article = page_obj.paginate_queryset(queryset=article_list, request=request, view=self)
        # article_serializer = BlogArticleSerializer(page_article, many=True)
        # total_cnt = len(article_serializer.data)

        # return Response({'code': 20000, "data": article_serializer.data, "total_cnt": total_cnt},
        #                 status=status.HTTP_200_OK)
        return api_paging(article_list, request, BlogArticleSerializer)

    def post(self, request, format=None):
        article_serializer = BlogArticleSerializer(data=request.data)
        if article_serializer.is_valid():
            article_serializer.save()
            return Response({'code': 20000, "data": article_serializer.data}, status=status.HTTP_200_OK)
        return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogArticleDetailView(APIView):
    def get(self, request, article_id):
        try:
            article_list = BlogArticle.objects.get(id=article_id)
            article_serializer = BlogArticleSerializer(article_list)
            return Response({'code': 20000, "data": article_serializer.data},
                            status=status.HTTP_200_OK)
        except:
            raise Http404


class BlogArticleDetailViewByClass(APIView):
    def get(self, request):
        try:
            class_id = request.GET.get('class_id')
            key_words = request.GET.get('key_words')
            print(request.GET)
            if class_id:
                article_list = BlogArticle.objects.filter(is_platform=class_id)
                article_serializer = BlogArticleSerializer(article_list, many=True)
                return Response({'code': 20000, "data": article_serializer.data},
                                status=status.HTTP_200_OK)
            if key_words:
                article_list = BlogArticle.objects.filter(title__contains=key_words)
                article_serializer = BlogArticleSerializer(article_list, many=True)
                return Response({'code': 20000, "data": article_serializer.data},
                                status=status.HTTP_200_OK)
        except:
            raise Http404


class BlogArticlePlatformView(APIView):
    def get(self, request):
        try:
            platform_list = BlogArticlePlatform.objects.all()
            platform_serializer = BlogArticlePlatformSerializer(platform_list, many=True)
            return Response({'code': 20000, "data": platform_serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            raise Http404


class BlogNavMenuListView(APIView):
    def get(self, request):
        try:
            blognavmenu_list = BlogNavMenuList.objects.all()
            blognavmenu__serializer = BlogNavMenuListSerializer(blognavmenu_list, many=True)
            return Response({'code': 20000, "data": blognavmenu__serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            raise Http404


class BloFriendsView(APIView):
    def get(self, request):
        try:
            blogfriends_list = BlogFriends.objects.all()
            blogfriends_serializer = BlogFriendsSerializer(blogfriends_list, many=True)
            return Response({'code': 20000, "data": blogfriends_serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            raise Http404


class BlogAboutMeView(APIView):
    def get(self, request):
        try:
            blogAboutMe_list = BlogAboutMe.objects.get(id=1)
            blogAboutMe_serializer = BlogAboutMeSerializer(blogAboutMe_list)
            return Response({'code': 20000, "data": blogAboutMe_serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            raise Http404


class BlogUploadView(APIView):
    """
    https://blog.csdn.net/Monster_ixx/article/details/104601881
    """

    def post(self, request):
        fileDict = request.FILES.items()  # <MultiValueDict: {'file': [<InMemoryUploadedFile: k8s.jpg (image/jpeg)>]}>
        path = request.query_params.dict().get('path', '')
        for (k, v) in fileDict:
            # print("dic[%s]=%s" % (k, v))
            fileData = request.FILES.getlist(k)
            for file in fileData:
                fileName = file._get_name()
                filePath = os.path.join(MEDIA_ROOT + path, fileName)
                logger.info('filepath = [%s]' % filePath)
                try:
                    writeFile(filePath, file)
                except Exception as e:
                    logger.error(e)
                    return Response({'code': 20001, "data": {'file': '文件上传失败'}}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'code': 20000, "data": {'file': fileName}}, status=status.HTTP_200_OK)


class RegisterView(View):
    @staticmethod
    @get_request_body
    def post(request):
        # print(request.POST)
        user_name = request.POST.get('username', '')
        user_password = request.POST.get('password', '')
        user_email = request.POST.get('email', '')
        user_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(10, 99))
        # 判断邮箱是否已被注册
        if BlogUserInfo.objects.filter(email=user_email):
            return JsonResponse({'code': 20001, "data": "邮箱已被注册"}, status=200)
        else:
            # 入库
            BlogUserInfo.objects.create(user_name=user_name, email=user_email, password=user_password,
                                        register_time=datetime.datetime.now(), user_id=user_id)
            # 异步推送邮件
            scheduler = BackgroundScheduler()

            # 首先生成jwt token
            user_token = create_token(user_id=user_id, email=user_email)
            logger.info("user_token:".format(user_token))
            # 根据token生成拼接话术
            text_content, html_content = create_message(token=user_token)
            logger.info("text_content:{0}\n html_content:{1}".format(text_content, html_content))
            logger.info("开始发邮件咯")
            scheduler.add_job(send_mail, args=(
                '小彬彬博客注册激活邮件', text_content, 'yangyubin1@126.com(小彬彬的博客)', [user_email], html_content), trigger='date',
                              next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=3))
            scheduler.start()
            return JsonResponse({'code': 20000, "data": "ok"}, status=200)


class ActivateView(View):
    @staticmethod
    def get(request):
        user_token = (request.GET.get('token'))
        user_pay_load, _ = authenticate(user_token)
        # print(user_pay_load)
        # 获取 user_pay_load中的user_id去更新user表中的激活状态
        # 如果不为空就更新激活状态
        if user_pay_load:
            BlogUserInfo.objects.filter(user_id=user_pay_load.get('user_id')).update(status='1')
            # return redirect("http://localhost:9528/#/UserLogin?login=1")
            return redirect("http://blog.yybgzh.cn/#/UserLogin?login=1")
        else:
            return JsonResponse({'code': 20002, "data": "fail", "msg": "激活失败"}, status=200)
            # return JsonResponse({'code': 20000, "data": "ok", "msg": "激活成功"}, status=200)


# https://www.lagou.com/lgeduarticle/33837.html values
class LoginView(View):
    @staticmethod
    def get(request):
        user_email = request.GET.get('email')
        user_password = request.GET.get('password')
        # 验证密码是否一致
        if BlogUserInfo.objects.get(email=user_email, password=user_password):
            user_info = BlogUserInfo.objects.filter(email=user_email, password=user_password)
            # 偷懒办法从queryset中获取userid和usr_name
            user_id = user_info.values('user_id')[0].get('user_id')
            user_name = user_info.values('user_name')[0].get('user_name')
            label = user_info.values('label')[0].get('label')
            avatar = user_info.values('avatar')[0].get('avatar')

            return JsonResponse(
                    {'code': 20000,
                     "data": {"userId": user_id, "user_name": user_name, "label": label, "avatar": avatar},
                     "msg": "激活成功"},
                    status=200)
        else:
            return JsonResponse({'code': 20001, "data": "fail", "msg": "登录失败，请检查信息是否一致"}, status=200)


class GetUserInfoView(APIView):
    """
    https://blog.csdn.net/Monster_ixx/article/details/104601881
    """

    @staticmethod
    def get(request):
        try:
            # print(request.query_params.dict())
            userid = request.GET.dict().get('userID')
            blog_user_list = BlogUserInfo.objects.filter(user_id=userid)
            blog_user_serializer = BlogUserSerializer(blog_user_list, many=True)
            return Response({'code': 20000, "data": blog_user_serializer.data},
                            status=status.HTTP_200_OK)
        except:
            raise Http404


# 试试drf的方法 https://www.cnblogs.com/BlueSkyyj/p/11385874.html
class UserUpdateView(APIView):
    def put(self, request, *args, **kwargs):
        user_info = BlogUserInfo.objects.filter(user_id=request.data.get('user_id')).first()
        obj = BlogUserSerializer(data=request.data, instance=user_info, partial=True)
        if obj.is_valid():
            obj.save()
            return Response({'code': 20000, "data": obj.data, "msg": "更新成功"}, status=status.HTTP_200_OK)
        else:
            return Response({'code': 20001, "data": obj.errors, "msg": "更新异常"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 文章点赞和喜欢
class BlogLikeCollectViewSet(APIView):
    def get(self, request, format=None):
        # 获取get参数中的userid以及islike
        user_id = request.query_params.dict().get('user_id')
        islike = request.query_params.dict().get('islike')
        article_id = request.query_params.dict().get('art_id')

        db_instance = MysqlDataBase(host=DATABASE_SC_URL.get('HOST'), user=DATABASE_SC_URL.get('USERNAME'),
                                    password=DATABASE_SC_URL.get('PASSWD'), port=DATABASE_SC_URL.get('PORT'),
                                    db=DATABASE_SC_URL.get('DB'))
        if int(article_id) == 0:
            sql = "select a.id,a.create_time,a.title,a.guest_count,a.comment_count,a.like_count,a.collect_count,a.content_short,a.image_url from myblog_article a, myblog_likeCollect b " \
                  "where a.id =b.article_id  and b.islike={0} and b.user_id={1} order by b.article_id desc".format(
                    islike, user_id)
        else:
            sql = "select a.id,a.create_time,a.title,a.guest_count,a.comment_count,a.like_count,a.collect_count,a.content_short,a.image_url from myblog_article a, myblog_likeCollect b " \
                  "where a.id =b.article_id  and b.islike={0} and b.user_id={1} and b.article_id<{2}  order by b.article_id desc".format(
                    islike, user_id, article_id)
        result_list = db_instance.pd_read_sql(sql=sql)
        db_instance.close_db()

        #
        #     article_list = BlogCollectLikeInfo.objects.filter(user_id=user_id, islike=islike, ).order_by(
        #             "-id")[0:3]  #
        # else:
        #     article_list = BlogCollectLikeInfo.objects.filter(user_id=user_id, islike=islike,
        #                                                       article_id__lt=article_id).order_by(
        #             "-id")[0:3]
        # article_serializer = BlogCollectLikeSerializer(article_list, many=True)
        total_cnt = len(result_list)
        if total_cnt:
            return Response(
                    {'code': 20000, "data": result_list[0:3], "msg": "查询成功", "total": total_cnt},
                    status=status.HTTP_200_OK)
        else:
            return Response(
                    {'code': 20001, "data": [], "msg": "没有更多结果了", "total": total_cnt},
                    status=status.HTTP_200_OK)

    def post(self, request, format=None):
        # 获取post参数中的userid以及islike以及article_id
        user_id = request.data.get('user_id')
        islike = request.data.get('islike')
        article_id = request.data.get('article_id')
        likeart = request.data.get('likeArt')  # true表示点击喜欢  false表示取消
        collectart = request.data.get('collectArt')  # true表示点击收藏 false表示取消

        article_serializer = BlogCollectLikeSerializer(data=request.data)
        if article_serializer.is_valid():
            if islike == 1:
                if likeart:
                    article_serializer.save()
                    BlogArticle.objects.filter(id=article_id).update(like_count=F('like_count') + 1)
                    return Response({'code': 20000, "data": article_serializer.data, "msg": "点赞成功"},
                                    status=status.HTTP_200_OK)
                else:
                    BlogCollectLikeInfo.objects.get(user_id=user_id, islike=islike, article_id=article_id).delete()
                    BlogArticle.objects.filter(id=article_id).update(like_count=F('like_count') - 1)
                    return Response({'code': 20000, "data": article_serializer.data, "msg": "取消点赞成功"},
                                    status=status.HTTP_200_OK)
            else:
                # 如果取消,删除该条记录
                # 并修改文章信息表的相应次数
                if collectart:
                    article_serializer.save()
                    BlogArticle.objects.filter(id=article_id).update(collect_count=F('collect_count') + 1)
                    return Response({'code': 20000, "data": article_serializer.data, "msg": "收藏成功"},
                                    status=status.HTTP_200_OK)
                else:
                    BlogCollectLikeInfo.objects.get(user_id=user_id, islike=islike, article_id=article_id).delete()
                    BlogArticle.objects.filter(id=article_id).update(collect_count=F('collect_count') - 1)
                    return Response({'code': 20000, "data": article_serializer.data, "msg": "取消收藏成功"},
                                    status=status.HTTP_200_OK)
        return Response({'code': 20001, "data": article_serializer.errors, "msg": "请求异常"},
                        status=status.HTTP_400_BAD_REQUEST)
        # return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnalyzeLikeCollectViewSet(View):
    @staticmethod
    def get(request):
        user_article = request.GET.get('article_id')
        user_id = request.GET.get('user_id')
        data = {}
        # 验证密码是否一致
        if BlogCollectLikeInfo.objects.filter(article_id=user_article, user_id=user_id, islike='1'):
            data['like_bj'] = 1
        else:
            data['like_bj'] = 0

        if BlogCollectLikeInfo.objects.filter(article_id=user_article, user_id=user_id, islike='2'):
            data['collect_bj'] = 1
        else:
            data['collect_bj'] = 0
        return JsonResponse({'code': 20000, "data": data, "msg": "查询成功"}, status=200)


class ArticleCommentView(View):
    @staticmethod
    def get(request):
        article_id = request.GET.get('article_id')
        comment_id = request.GET.get('comment_id')

        db_instance = MysqlDataBase(host=DATABASE_SC_URL.get('HOST'), user=DATABASE_SC_URL.get('USERNAME'),
                                    password=DATABASE_SC_URL.get('PASSWD'), port=DATABASE_SC_URL.get('PORT'),
                                    db=DATABASE_SC_URL.get('DB'))
        sql = "select * from " \
              "(select * from myblog_comment a  where a.article_id= {0} and a.parent_comment_id=0 " \
              "union all " \
              "select * from myblog_comment a  where a.article_id={0} and a.parent_comment_id<>0) aa order by  parent_comment_id ,time desc".format(
                article_id)
        result_list = db_instance.pd_read_sql(sql=sql)
        db_instance.close_db()
        if result_list:
            # sql搞不定逻辑，所以用程序来处理，默认dataframe读进去，读满list跑路走人
            # 循环读取，循环第一条的时候，要重新去找一下parement_id是否存在id为1的数据，如果存在放入到childson，否则为空list
            # 循环，只处理pid为0的数据，如果碰到>0的就不处理，超过5条就退出（假设分页为5）
            try:
                mylist = []
                for n in range(0, len(result_list)):
                    myDict = {'comment_id': result_list[n].get('id'), 'avatar': result_list[n].get('avatar'),
                              'username': result_list[n].get('username'), 'label': result_list[n].get('label'),
                              'time': result_list[n].get('time'), 'content': result_list[n].get('content'),
                              'ChildsSon': []}
                    # 等于0则记录
                    if result_list[n].get('parent_comment_id') == 0:
                        mylist.append(myDict)
                    else:
                        # 如果父节点非0，即有父节点的话，就要添加在父节点字典中的childson的list里面
                        get_comment_id(mylist, result_list[n].get('parent_comment_id'), myDict)
                        # if len(mylist) >= PAGE_SIZE:
                        #     print("准备退出")
                if int(comment_id) == 0:
                    result = mylist[0:PAGE_SIZE]
                else:
                    i = get_list_index(mylist, comment_id)
                    result = mylist[i + 1:i + 1 + PAGE_SIZE]

                return JsonResponse({'code': 20000, "data": result, "msg": "查询评论成功", "total": len(result)}, status=200)
            except Exception as e:
                logger.error("循环拼接comment列表信息出错，失败原因{}".format(e))
                return JsonResponse({'code': 20002, "data": [], "msg": "查询评论异常"}, status=200)
        else:
            return JsonResponse({'code': 20000, "data": [], "msg": "查询无数据"}, status=200)

    @staticmethod
    @get_request_body
    def post(request):
        content = request.POST.get('content')
        user_id = request.POST.get('user_id')
        user_name = request.POST.get('user_name')
        article_id = request.POST.get('article_id')
        pid = request.POST.get('pid')
        label = request.POST.get('label')
        avatar = request.POST.get('avatar')

        insert_content = {'avatar': avatar, 'user_id': user_id, 'username': user_name, 'label': label,
                          'content': content,
                          'parent_comment_id': pid, "article_id": article_id}
        ArticleComment.objects.create(**insert_content)
        comment = ArticleComment.objects.filter(article_id=article_id).order_by('-time').first()
        if article_id != 0:
            BlogArticle.objects.filter(id=article_id).update(comment_count=F('comment_count') + 1)
        return JsonResponse({'code': 20000, "data": {'comment_id': comment.id}, "msg": "保存评论成功"}, status=200)


class BlogGuestView(APIView):
    """
    https://blog.csdn.net/Monster_ixx/article/details/104601881
    """

    @staticmethod
    def get(request):
        try:
            guests_log = BlogGuestLog.objects.all()
            user_guest_serializer = BlogGuestLogSerializer(guests_log, many=True)
            return Response({'code': 20000, "data": user_guest_serializer.data},
                            status=status.HTTP_200_OK)
        except:
            raise Http404

    def post(self, request, format=None):
        article_id = request.data.get('article_id', '')
        blog_serializer = BlogGuestLogSerializer(data=request.data)
        if blog_serializer.is_valid():
            blog_serializer.save()
            BlogArticle.objects.filter(id=article_id).update(guest_count=F('guest_count') + 1)
            return Response({'code': 20000, "data": blog_serializer.data}, status=status.HTTP_200_OK)
        return Response(blog_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 文章取前10评论多的
class ArticleShowBrowseCount(APIView):
    def get(self, request, format=None):
        page_article = BlogArticle.objects.all().order_by("-guest_count")
        article_serializer = BlogArticleSerializer(page_article, many=True)
        return Response({'code': 20000, "data": article_serializer.data[0:10]}, status=status.HTTP_200_OK)


# 评论取前10多的
class ArticleShowComment(APIView):
    @staticmethod
    def get(request):
        article_comment = ArticleComment.objects.all().order_by("-time")
        # article_serializer = Blog(article_comment, many=True)
        comment_list = list(article_comment.values())
        db_instance = MysqlDataBase(host=DATABASE_SC_URL.get('HOST'), user=DATABASE_SC_URL.get('USERNAME'),
                                    password=DATABASE_SC_URL.get('PASSWD'), port=DATABASE_SC_URL.get('PORT'),
                                    db=DATABASE_SC_URL.get('DB'))
        sql = "select b.id,a.avatar,a.username,b.title,a.content from myblog_comment a,myblog_article b " \
              "where a.article_id = b.id order by a.time desc "
        result_list = db_instance.pd_read_sql(sql=sql)
        db_instance.close_db()
        return Response({'code': 20000, "data": result_list[0:10]}, status=status.HTTP_200_OK)


class BlogLikeNumView(View):
    @staticmethod
    def get(request):
        result = BlogLikeNum.objects.first()
        return JsonResponse({'code': 20000, "data": {'like_num': result.like_num}, "msg": "ok"}, status=200)

    @staticmethod
    @get_request_body
    def post(request):
        like_num = request.POST.get('like_num')
        BlogLikeNum.objects.filter(id=1).update(like_num=F('like_num') + like_num)
        return JsonResponse({'code': 20000, "data": "ok", "msg": "ok"}, status=200)
