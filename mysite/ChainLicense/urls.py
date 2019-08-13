from django.urls import path

from . import views

urlpatterns = [
    # main
    path('', views.index, name='index'),
    path('ChainLicense/new', views.post_new, name='post_new'),
    path('ChainLicense/compare', views.post_compare, name='post_compare'),
    path('ChainLicense/<int:seq>/', views.post_detail, name='post_detail'),
    path('ChainLicense/list', views.post_list, name='post_list'),
    # /s_parser/java/
    #path('<cha:languageName>/', views.detail, name='detail'),
]
