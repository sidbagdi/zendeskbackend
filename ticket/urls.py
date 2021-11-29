from django.urls import path

from . import views
from .views import TicketListView

urlpatterns = [
    # path('',url(r'^search/', search),url(r'^index/', index)),
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    # path('allTickets', views.getAllTickets, name='allTickets'),
    path('allTickets', TicketListView.as_view()),
    # path('<int:ticket_id>/', views.detail, name='detail')
    # ex: /polls/5/results/
    # path('<int:id>/', views.search, name='detail'),
    # path('<int:id>/', views.response, name='id'),
]