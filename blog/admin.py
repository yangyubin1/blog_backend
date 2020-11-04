from django.contrib import admin
from .models import Recipe, BlogArticle, BlogArticlePlatform, BlogNavMenuList, BlogFriends, BlogAboutMe, BlogUserInfo, \
    BlogCollectLikeInfo, ArticleComment,BlogGuestLog

# Register your models here.
admin.site.register(Recipe)
admin.site.register(BlogArticle)
admin.site.register(BlogArticlePlatform)
admin.site.register(BlogNavMenuList)
admin.site.register(BlogFriends)
admin.site.register(BlogAboutMe)
admin.site.register(BlogUserInfo)
admin.site.register(BlogCollectLikeInfo)
admin.site.register(ArticleComment)
admin.site.register(BlogGuestLog)


