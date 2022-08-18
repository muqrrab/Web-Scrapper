from django.urls import path
from django.conf.urls import include
from . import views


app_name = 'scrape'
urlpatterns = [
    path('', views.index, name="index"),
    path('<int:id>', views.detail, name="detail")
]
