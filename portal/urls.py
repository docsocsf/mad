from django.conf.urls import url

from portal import views

app_name = 'portal'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<position>parent|child)/$', views.index, name='index'),
    url(r'^preferences/(?P<id>[0-9a-zA-Z]{8})', views.preferences, name='preferences')
]
