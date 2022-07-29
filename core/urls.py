from django.urls import path
from . import views
from django.contrib import admin

urlpatterns=[
    path('',views.home,name='home'),
    path('problems/tag=<str:tag>/page=<int:id>&sortby=<str:sortby>&reverse=<str:reverse>',views.problems,name='problems'),
    path('contests/page=<int:id>/<str:url_str>',views.contests,name='contests'),
]
