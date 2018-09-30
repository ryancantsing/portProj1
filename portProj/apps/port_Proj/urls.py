from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^editUser$', views.edit_user),
    url(r'^status$', views.status),
    url(r'^user/(?P<user_id>\d+)$', views.user),
    url(r'^post$', views.post),
    url(r'^comment/(?P<post_id>\d+)$', views.add_comment),
    url(r'^delete$', views.delete_user),
    url(r'^deletepost/(?P<post_id>\d+)$', views.delete_post),
    url(r'^deletecomment/(?P<comment_id>\d+)$', views.delete_comment),
    url(r'^logout$', views.logout)
]

