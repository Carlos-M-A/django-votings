"""
voting URL Configuration
"""

from django.urls import path
from . import views

app_name = 'votings'
urlpatterns = [
    path('votings/', views.index, name='index'),
    path('votings/<int:voting_id>/', views.voting, name='voting'),
    path('votings/<int:voting_id>/options', views.options, name='options'),
    path('options/<int:pk>', views.OptionView.as_view(), name='option'),
]
