from django.conf.urls import url

from post import post_views

urlpatterns = [
    url(r'^index/', post_views.index),
    url(r'create/', post_views.create_post),
    url(r'^edit/', post_views.edit_post),
    url(r'^search/', post_views.search_post),
    url(r'^read/', post_views.read_post),
    url(r'^$', post_views.list_post),
]