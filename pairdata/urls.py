__author__ = 'akash'
from django.conf.urls import url
from . import views

urlpatterns = [
    url('pancake_data', views.pancake_data, name='pancake_data'),
]