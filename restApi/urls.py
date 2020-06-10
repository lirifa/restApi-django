# -*- coding: utf-8 -*-
"""restApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

#from django.conf.urls import url, include
from django.contrib import admin
from user import views as user_view
from article import views as article_view
from image import views as image_view



#urlpatterns = [
#    url(r'^admin/', admin.site.urls),
#    url(r'^api/user/login$', user_view.login), # 用户登录
#]
from django.conf.urls import url, include
from rest_framework import routers
from quickstart import views
from snippets.views import SnippetList 

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
#router.register(r'snippets/list', SnippetList, 'snippets')

urlpatterns = [
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),

    #用户相关接口
    url(r'^api/user/login$', user_view.login),
    url(r'^api/user/info$', user_view.userInfo),
    url(r'^api/user/update$', user_view.updateInfo),
    url(r'^api/user/logout$', user_view.logout),

    url(r'^api/admin/login$', user_view.adminLogin),

    #文章相关接口
    url(r'^api/article/allList$', article_view.allList),
    url(r'^api/article/list$', article_view.list),
    url(r'^api/article/detail$', article_view.articleDetail),
    url(r'^api/article/create$', article_view.create),
    url(r'^api/article/update$', article_view.update),
    url(r'^api/article/istop$', article_view.updateIsTop),
    url(r'^api/article/toplist$', article_view.fetchTopArticle),
    url(r'^api/platform/list$', article_view.platformList),

    #图片相关接口
    url(r'^api/image/upload$', image_view.imageUpload),
    url(r'^api/image/ossAll$', image_view.imageAll),
    url(r'^api/image/delete$', image_view.removeFile),
    url(r'^api/image/mkdir$', image_view.mkdir),
   
    #文件上传
    url(r'^api/file/upload$', image_view.fileUpload),
    #代码片段
    url('', include('snippets.urls')),
]
