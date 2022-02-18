"""
voting URL Configuration
"""

from unicodedata import name
from django.urls import path
from . import views

app_name = 'votings'
urlpatterns = [
    path('general/<int:general_assembly_id>', views.general_index, name='general_index'),
    path('assemblies/<int:assembly_id>/votings', views.assemblies_show, name='assemblies_show'),
    path('assemblies/<int:assembly_id>/votings/create', views.votings_create, name='votings_create'),

    path('votings/', views.votings_search, name='votings_search'),
    path('votings/<int:voting_id>/', views.votings_show, name='votings_show'),
    path('votings/<int:voting_id>/edit', views.votings_edit, name='votings_edit'),
    path('votings/<int:voting_id>/delete', views.votings_delete, name='votings_delete'),
    path('votings/<int:voting_id>/schedule', views.votings_schedule, name='votings_schedule'),
    path('votings/<int:voting_id>/unschedule', views.votings_unschedule, name='votings_unschedule'),

    path('votings/<int:voting_id>/options/create', views.options_create, name='options_create'),
    path('votings/<int:voting_id>/options/<int:option_id>/edit', views.options_edit, name='options_edit'),
    path('votings/<int:voting_id>/options/<int:option_id>/delete', views.options_delete, name='options_delete'),
    
    path('votings/<int:voting_id>/options/<int:option_id>/vote', views.votes_create, name='votes_create')
]
