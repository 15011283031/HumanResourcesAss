from django.conf.urls import url
from . import index

urlpatterns = [
    url(r'^index$',index.loginConfig),
    url(r'^saveNewConnecttion/$', index.saveNewConnecttion, name='saveNewConnecttion'),
]