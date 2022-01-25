"""
voting URL Configuration
"""

from django.urls import path
from . import views

app_name = 'votings'
urlpatterns = [
    path('votings/', views.votings_index, name='votings_index'),
    path('votings/create', views.votings_create, name='votings_create'),
    path('votings/<int:voting_id>/', views.votings_show, name='votings_show'),
    path('votings/<int:voting_id>/edit', views.votings_edit, name='votings_edit'),
    path('votings/<int:voting_id>/delete', views.votings_delete, name='votings_delete'),

    path('votings/<int:voting_id>/options/create', views.options_create, name='options_create'),
    path('votings/<int:voting_id>/options/<int:option_id>/edit', views.options_edit, name='options_edit'),
    path('votings/<int:voting_id>/options/<int:option_id>/delete', views.options_delete, name='options_delete')
]
