from django.conf.urls import url
from basic_app import views

# Template URLS
app_name = 'basic_app'

urlpatterns = [
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^register/$', views.register, name='register'),
]
