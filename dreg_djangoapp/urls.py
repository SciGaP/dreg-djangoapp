from django.conf.urls import url

from . import views

app_name = 'dreg_djangoapp'
urlpatterns = [
    url(r'^hello/', views.hello_world, name="hello"),
    url(r'^gbrowser/', views.gbrowser_dreg, name = 'gbrowser_dreg'),
    url(r'^gbfile/', views.gbfile_download, name = 'gbfile_download')
]
