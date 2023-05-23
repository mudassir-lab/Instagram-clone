"""instagramproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from instaapp import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'instapp'
urlpatterns = [

    path('admin/', admin.site.urls),
    path('signup/', views.create_profile, name='signup'),
    path('Login/', views.Login, name='Login'),
    path('Logout/', views.Logout, name='Logout'),
    path('home/', views.home, name='home'),
    path('profile/<username>', views.profile, name='profile'),
    path('search/', views.search, name='search'),
    path('follow/<str:username>', views.follow, name='follow'),
    path('uploadpost/', views.uploadpost, name='uploadpost'),
    path('likes/<id>', views.like, name='likes'),
    path('comments/<id>', views.comments, name='comments'),
    path('uploadstory/', views.uploadstory, name='uploadstory'),
    path('editprofile/', views.editprofile, name='editprofile'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
