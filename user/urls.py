from django.conf.urls import url

from user import user_views

urlpatterns = [
    url(r'^register/', user_views.register),
    url(r'^login/', user_views.login),
    url(r'^logout/', user_views.logout),
    url(r'^info/', user_views.user_info),
]