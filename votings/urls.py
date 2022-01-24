"""
voting URL Configuration
"""

from django.urls import path
from . import views

app_name = 'votings'
urlpatterns = [
    path('votings/', views.votings_index, name='votings.index'),
    path('votings/create', views.votings_create, name='votings.create'),
    path('votings/<int:voting_id>/', views.votings_show, name='votings.show'),
    path('votings/<int:voting_id>/edit', views.votings_edit, name='votings.edit'),
    path('votings/<int:voting_id>/delete', views.votings_delete, name='votings.delete'),

    path('votings/<int:voting_id>/options/create', views.options_create, name='options.create'),
    path('votings/<int:voting_id>/options/<int:option_id>/edit', views.options_edit, name='options.edit'),
    path('votings/<int:voting_id>/options/<int:option_id>/delete', views.options_delete, name='options.delete'),

    path('votings/<int:voting_id>/options', views.options, name='options'),
    path('options/<int:pk>', views.OptionView.as_view(), name='option'),
]
