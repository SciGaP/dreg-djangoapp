from django.conf.urls import url

from . import views

app_name = 'dreg_djangoapp'
urlpatterns = [
    url(r'^hello/', views.hello_world, name="hello"),
]
