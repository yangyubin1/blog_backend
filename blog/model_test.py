# -*- coding: utf-8 -*-
__author__ = 'yubin.yang'
__date__ = '2020/9/23 16:14'


# https://www.lagou.com/lgeduarticle/33837.html  python脚本中调用django环境
import os

# https://blog.csdn.net/Monster_ixx/article/details/104601881 django queryset转成json
#https://ops-coffee.cn/s/B_aNB8Y8snbSVLURONZ4Qg

# https://blog.csdn.net/LABLENET/article/details/56012774 分页查询

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_blog.settings")
    import django
    django.setup()

    from blog import models

    info = models.BlogUserInfo.objects.all()
    print(info) # queryset
    print(list(info.values()))
