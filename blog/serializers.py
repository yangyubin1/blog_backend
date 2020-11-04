# -*- coding: utf-8 -*-
__author__ = 'yubin.yang'
__date__ = '2020/8/21 14:30'

from rest_framework import serializers
from .models import Recipe, BlogArticle, BlogArticlePlatform, BlogNavMenuList, BlogFriends, BlogAboutMe, BlogUserInfo, \
    BlogCollectLikeInfo, BlogGuestLog


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'ingredients', 'picture',
            'difficulty', 'prep_time', 'prep_guide'
        )


class BlogArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogArticle
        # field = '__all__'
        fields = (
            'id', 'is_comment', 'status', 'is_platform',
            'title', 'author', 'display_time', 'importance', 'content_short', 'content',
            'image_url', 'create_time', 'update_time', 'like_count', 'guest_count', 'comment_count', 'collect_count','cate_name'
        )


class BlogArticlePlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogArticlePlatform
        # field = '__all__'
        fields = ('platform_id', 'platform_desc', 'platform_child')


class BlogNavMenuListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogNavMenuList
        # field = '__all__'
        fields = ('id', 'nav_name', 'nav_url')


class BlogFriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogFriends
        # field = '__all__'
        fields = ('id', 'image', 'name', 'description', 'url')


class BlogAboutMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogAboutMe
        # field = '__all__'
        fields = ('id', 'brief', 'image')


class BlogUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogUserInfo
        fields = (
            'id', 'user_id', 'user_name', 'email', 'password', 'register_time', 'sex', 'label', 'avatar', 'status')

    def update(self, instance, validated_data):
        instance.user_name = validated_data.get('user_name', instance.user_name)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.email = validated_data.get('email', instance.email)
        instance.sex = validated_data.get('sex', instance.sex)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.label = validated_data.get('label', instance.label)
        instance.save()
        return instance


class BlogCollectLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCollectLikeInfo
        # field = '__all__'
        fields = ('id', 'user_id', 'article_id', 'create_time', 'update_time', 'islike')


class BlogGuestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogGuestLog
        # field = '__all__'
        fields = ('id', 'user_name', 'article_id', 'guest_time')
