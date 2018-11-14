from django.urls import path

from wiki import views

app_name = 'wiki'

urlpatterns = [

    path('', views.index, name='index'),
]
