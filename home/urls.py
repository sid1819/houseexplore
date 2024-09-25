from django.contrib import admin
from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='home'),
    path('signup',views.signup,name='signup'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('search',views.search,name='search'),
    path('search2',views.search2,name='search2'),
    path('dealerinfo',views.dealerinfo,name='dealerinfo'),
    path('aboutus',views.aboutus,name='aboutus'),
    path('contactus',views.contactus,name='contactus'),
    path('addhouse',views.addhouse,name='addhouse'),
    path('myhouses',views.myhouses,name='myhouses'),
    path('remove_house/<str:house_id>/',views.remove_house,name='remove_house'),
    path('chat/<int:recipient_id>/', views.chat, name='chat'),
    path('send_message/<int:recipient_id>/', views.send_message, name='send_message'),
    path('chat_users/', views.chat_users, name='chat_users'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
