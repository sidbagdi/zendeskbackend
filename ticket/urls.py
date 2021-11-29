from django.urls import path, re_path

from . import views
# from .views import TicketListView

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('allTickets', views.ticket_listing, name='ticket_listing'),
    re_path(r'^(?P<path>.*)/$',  views.index, name='index'),

]