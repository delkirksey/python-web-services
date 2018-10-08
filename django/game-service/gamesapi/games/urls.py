from django.conf.urls import url

from games import views

# urlpatterns must be defined as "urlpatterns" exactly
urlpatterns = [
    url(r'^games/$', views.game_list),
    url(r'^games/(?P<pk>[0-9]+)/$', views.game_detail),
]
