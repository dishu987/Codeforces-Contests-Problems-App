from django.urls import path
from core import views
from django.contrib import admin
from django.urls import re_path as url
from django.conf import settings
from django.views.static import serve

urlpatterns=[
    path('',views.home,name='home'),
    path('problems/tag=<str:tag>/page=<int:id>&sortby=<str:sortby>&reverse=<str:reverse>',views.problems,name='problems'),
    path('contests/page=<int:id>/<str:url_str>',views.contests,name='contests'),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]


