from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index')
    path('/current', views.current, name='current')
    path('/combined', views.combined, name='combined')
    path('/default_screen', views.defaultscreen, name='default_screen')
    path('/graphics', views.graphics, name='graphics')
    path('/custom_content', views.custom_content, name='custon_content')
]
