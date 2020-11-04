# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
import datetime


# Create your models here.

class Recipe(models.Model):
    DIFFICULTY_LEVELS = (
        ('Easy', '容易'),
        ('Medium', '中等'),
        ('Hard', '困难'),
    )
    name = models.CharField(max_length=120, verbose_name='名称')
    ingredients = models.CharField(max_length=400, verbose_name='食材')
    picture = models.FileField(verbose_name='图片')
    difficulty = models.CharField(choices=DIFFICULTY_LEVELS, max_length=10,
                                  verbose_name='制作难度')
    prep_time = models.PositiveIntegerField(verbose_name='准备时间')
    prep_guide = models.TextField(verbose_name='制作指南')

    class Meta:
        verbose_name = '食谱'
        verbose_name_plural = '食谱'

    def __str__(self):
        return '{} 的食谱'.format(self.name)


class BlogArticle(models.Model):
    comment_choice = (
        ('Y', '是'),
        ('N', '不是')
    )
    status_choice = (('0', '未发布'),
                     ('1', '已发布'))
    platform_choice = (('01', '技术'),
                       ('02', '冷知识'), ('03', '新闻'), ('04', '娱乐'))
    importance_choice = (('1', '一颗星'),
                         ('2', '两颗星'), ('3', '三颗星'), ('4', '四颗星'), ('5', '五颗星'))

    is_comment = models.CharField(choices=comment_choice, max_length=1,
                                  verbose_name='是否开启评论')
    status = models.CharField(choices=status_choice, max_length=1,
                              verbose_name='是否发布')
    is_platform = models.CharField(choices=platform_choice, max_length=2,
                                   verbose_name='文章分类')
    title = models.CharField(max_length=50, verbose_name='标题')
    author = models.CharField(max_length=20, verbose_name='作者')
    display_time = models.DateTimeField(verbose_name="发布时间", null=True, blank=True)
    importance = models.CharField(choices=importance_choice, max_length=1,
                                  verbose_name='重要性', default='1')
    content_short = models.CharField(max_length=100, verbose_name='文章简述', null=True, blank=True)
    content = models.TextField(verbose_name='文章内容', null=True, blank=True)
    image_url = models.CharField(max_length=50, verbose_name='图片地址', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    like_count = models.IntegerField(default=0, verbose_name='点赞次数', null=True, blank=True)
    guest_count = models.IntegerField(default=0, verbose_name='访问次数', null=True, blank=True)
    comment_count = models.IntegerField(default=0, verbose_name='评论次数', null=True, blank=True)
    collect_count = models.IntegerField(default=0, verbose_name='收藏次数', null=True, blank=True)
    cate_name = models.CharField(max_length=50, verbose_name='小标签', null=True, blank=True)

    class Meta:
        db_table = 'myblog_article'
        verbose_name = '博客文章基本信息表'
        verbose_name_plural = '博客文章基本信息表'

    def __str__(self):
        return self.title


class BlogArticlePlatform(models.Model):
    platform_id = models.CharField(max_length=2, verbose_name='分类编号')
    platform_desc = models.CharField(max_length=100, verbose_name='分类描述')
    platform_child = models.CharField(max_length=500, verbose_name='分类子类')

    class Meta:
        db_table = 'myblog_article_platform'
        verbose_name = '博客文章分类信息表'
        verbose_name_plural = '博客文章分类信息表'

    def __str__(self):
        return self.platform_desc


class BlogNavMenuList(models.Model):
    nav_name = models.CharField(max_length=50, verbose_name='项目名称')
    nav_url = models.CharField(max_length=200, verbose_name='URL地址')

    class Meta:
        db_table = 'myblog_navmenlist'
        verbose_name = '实验项目信息表'
        verbose_name_plural = '实验项目信息表'

    def __str__(self):
        return self.nav_name


class BlogFriends(models.Model):
    image = models.CharField(max_length=500, verbose_name='头像地址')
    name = models.CharField(max_length=50, verbose_name='朋友名字')
    description = models.CharField(max_length=100, verbose_name='描述')
    url = models.CharField(max_length=500, verbose_name='个人网站')

    class Meta:
        db_table = 'myblog_friends'
        verbose_name = '博客朋友列表'
        verbose_name_plural = '博客朋友列表'

    def __str__(self):
        return self.name


class BlogAboutMe(models.Model):
    brief = models.CharField(max_length=500, verbose_name='简介')
    image = models.CharField(max_length=500, verbose_name='图像地址')

    class Meta:
        db_table = 'myblog_aboutMe'
        verbose_name = '个人简介'
        verbose_name_plural = '个人简介'

    def __str__(self):
        return '杨宇斌'


class BlogUserInfo(models.Model):
    user_id = models.CharField(max_length=16, verbose_name='用户ID')
    user_name = models.CharField(max_length=30, verbose_name='用户姓名')
    email = models.CharField(max_length=200, verbose_name='邮箱地址')
    password = models.CharField(max_length=20, verbose_name='邮箱地址')
    register_time = models.DateTimeField(null=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    sex = models.CharField(max_length=10, default='男', verbose_name='性别')
    label = models.CharField(max_length=50, default='小萌新', verbose_name='标签')
    avatar = models.CharField(max_length=50, default='boy.png', verbose_name='头像')
    status = models.CharField(max_length=1, default='0', verbose_name='激活状态')

    class Meta:
        db_table = 'myblog_user'
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'

    def __str__(self):
        return self.user_name


class BlogCollectLikeInfo(models.Model):
    user_id = models.CharField(max_length=20, verbose_name='用户ID')
    article_id = models.IntegerField(verbose_name='文章ID')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    islike = models.CharField(max_length=1, verbose_name='点赞1收藏2')

    class Meta:
        db_table = 'myblog_likeCollect'
        verbose_name = '用户点赞收藏表'
        verbose_name_plural = '用户点赞收藏表'

    def __str__(self):
        return self.user_id + '文章id:' + str(self.article_id) + ' 类型是:' + '点赞' if self.islike == '1' else '收藏'


class ArticleComment(models.Model):
    avatar = models.CharField(max_length=500, verbose_name='用户头像')
    user_id = models.CharField(max_length=20, verbose_name='用户ID')
    username = models.CharField(max_length=100, verbose_name='用户姓名')
    label = models.CharField(max_length=30, verbose_name='用户标签')
    content = models.CharField(max_length=1000, verbose_name='评论内容')
    parent_comment_id = models.IntegerField(verbose_name='父节点评论ID')
    article_id = models.IntegerField(verbose_name='文章ID')
    time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'myblog_comment'
        verbose_name = '用户评论表'
        verbose_name_plural = '用户评论表'

    def __str__(self):
        return '文章id为：' + str(self.article_id) + '的评论信息'


class BlogGuestLog(models.Model):
    user_name = models.CharField(max_length=50, verbose_name='访客姓名')
    article_id = models.IntegerField(verbose_name='文章ID')
    guest_time = models.DateTimeField(auto_now_add=True, verbose_name='访问时间')

    class Meta:
        db_table = 'myblog_guest_log'
        verbose_name = '博客访客日志表'
        verbose_name_plural = '博客访客日志表'

    def __str__(self):
        return self.user_name


class BlogLikeNum(models.Model):
    like_num = models.IntegerField(verbose_name='点赞数量')

    class Meta:
        db_table = 'myblog_likenum'
        verbose_name = '点赞数量'
        verbose_name_plural = '点赞数量'

    # def __str__(self):
    #     return self.like_num
