# -*- coding: utf-8 -*-
__author__ = 'yubin.yang'
__date__ = '2020/8/21 14:45'
from django.conf.urls import url, include
# from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet, BlogArticleViewSet, TestView, BlogArticleDetailView, BlogArticlePlatformView, \
    BlogArticleDetailViewByClass, BlogNavMenuListView, BloFriendsView, BlogAboutMeView, BlogUploadView, RegisterView, \
    ActivateView, LoginView, GetUserInfoView, UserUpdateView, BlogLikeCollectViewSet, AnalyzeLikeCollectViewSet, \
    ArticleCommentView, BlogGuestView, ArticleShowBrowseCount,ArticleShowComment,BlogLikeNumView

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)
# router.register(r'blog_article', BlogArticleViewSet)

urlpatterns = [
    url('', include(router.urls), ),
    url(r'^test', TestView.as_view()),
    url(r'^blog_article/$', BlogArticleViewSet.as_view()),  # 博客文章
    url(r'^article_detail/(?P<article_id>\d+)/$', BlogArticleDetailView.as_view()),  # 博客文章详细
    url(r'^blog_article_platform', BlogArticlePlatformView.as_view()),  # 博客文章类别
    url(r'^article_platfrom/$', BlogArticleDetailViewByClass.as_view()),  # 根据文章类别查询博客文章
    url(r'^navMenList', BlogNavMenuListView.as_view()),  # 子菜单接口
    url(r'^Friends', BloFriendsView.as_view()),  # 我的偶像
    url(r'^AboutMeData', BlogAboutMeView.as_view()),  # 关于我接口
    url(r'^upload/$', BlogUploadView.as_view()),  # 图片上传接口
    url(r'^Register/$', RegisterView.as_view()),  # 图片上传接口
    url(r'^activate/$', ActivateView.as_view()),
    url(r'^login/$', LoginView.as_view()),
    url(r'^getUserInfo/$', GetUserInfoView.as_view()),  # 根据用户id查询用户详细情况
    url(r'^UserUpdate/$', UserUpdateView.as_view()),  # 修改用户信息
    url(r'^blog_collectLike/$', BlogLikeCollectViewSet.as_view()),  # 博客点赞和收藏
    url(r'^analyze_collectLike/$', AnalyzeLikeCollectViewSet.as_view()),  # 博客点赞和收藏
    url(r'^ArticleComment/$', ArticleCommentView.as_view()),  # 评论
    url(r'^guest_log/$', BlogGuestView.as_view()),  # 记录日志
    url(r'^article_showBrowseCount/$', ArticleShowBrowseCount.as_view()),  # 记录日志
    url(r'^article_ShowArtCommentCount/$', ArticleShowComment.as_view()),  # 记录日志
    url(r'^showLikeData/$', BlogLikeNumView.as_view()),  # 记录日志

]
