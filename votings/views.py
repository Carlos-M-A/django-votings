from calendar import month
from datetime import timedelta
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.core.exceptions import PermissionDenied, SuspiciousOperation, BadRequest
from django.db.models import Q
from .models import Assembly, Option, Organization, Participation, Vote, Voting, VotingStates
from .forms import OptionForm, SearchVotingForm, VotingDatesForm, VotingForm
from django.contrib.auth.models import User

def organizations_show(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)
    assemblies = organization.assembly_set.all()
    context = {
        'organization':organization,
        'assemblies':assemblies
    }
    return render(request, 'votings/organization_show.html', context)

def organization_create(request):
    pass

def assemblies_show(request, assembly_id):
    assembly = get_object_or_404(Assembly, pk=assembly_id)
    new_voting_form = VotingForm()
    planned_votings = assembly.voting_set.filter(state=VotingStates.PLANNED)
    scheduled_votings = assembly.voting_set.filter(state=VotingStates.SCHEDULED).order_by('start_date')
    active_votings = assembly.voting_set.filter(state=VotingStates.ACTIVE)
    finished_votings = assembly.voting_set.filter(state=VotingStates.FINISHED).order_by('-start_date')
    context = {
        'assembly':assembly,
        'new_voting_form':new_voting_form,
        'planned_votings':planned_votings,
        'scheduled_votings':scheduled_votings,
        'active_votings':active_votings,
        'finished_votings':finished_votings,
    }
    return render(request, 'votings/assemblies_show.html', context)

def votings_search(request):
    form = SearchVotingForm(request.GET)
    if form.is_valid():
        text = form.cleaned_data['text']
        state = form.cleaned_data['state']
        date_since = form.cleaned_data['date_since']
        date_until = form.cleaned_data['date_until']
        
        voting_list = Voting.objects.filter(Q(title_text__icontains=text) | Q(question_text__icontains=text))
        if date_since != None:
            voting_list = voting_list.filter(start_date__gt=date_since)
        if date_until != None:
            date_until += timedelta(days=1)
            voting_list = voting_list.filter(start_date__lt=date_until)
        if len(state) > 0 and int(state) > 0:
                voting_list = voting_list.filter(state=int(state))
        
        if date_since != None or date_until != None:
            voting_list = voting_list.order_by('start_date')
        elif len(state) > 0:
            state = int(state)
            if state == 0:
                voting_list = voting_list.order_by('-start_date')
            elif state == VotingStates.FINISHED:
                voting_list = voting_list.order_by('-start_date')
            elif state == VotingStates.SCHEDULED:
                voting_list = voting_list.order_by('start_date')
        else:
            voting_list = voting_list.order_by('-start_date')
        
        context = {
            'form':form,
            'voting_list':voting_list,
        }

        return render(request, 'votings/votings_search.html', context)

    else:
        raise BadRequest()

def votings_create(request, assembly_id):
    assembly = get_object_or_404(Assembly, pk=assembly_id)
    if request.method == "POST":
        form = VotingForm(request.POST)
        if form.is_valid():
            voting = form.save(commit=False)
            voting.assembly = assembly
            voting.electorate_quantity = 0
            voting.votes_quantity = 0
            voting.state = VotingStates.PLANNED
            voting.save()
            return redirect('votings:votings_show', voting_id=voting.id)
    else:
        form = VotingForm()
    context = {
        'form':form,
        'assembly':assembly
    }
    return render(request, 'votings/votings_create.html', context)

def votings_show(request, voting_id):
    try:
        voting:Voting = Voting.objects.get(pk=voting_id)
        options = voting.option_set.all()
        edit_voting_form = VotingForm(instance=voting)
        new_option_form = OptionForm()
        calendar_voting_form = VotingDatesForm(instance=voting)
        edit_option_forms = dict()
        for option in options:
            form_edit = OptionForm(instance=option)
            edit_option_forms[option.id] = form_edit

        context = {
            'voting':voting,
            'options':options,
            'new_option_form':new_option_form,
            'edit_option_forms':edit_option_forms,
            'edit_voting_form':edit_voting_form,
            'calendar_voting_form':calendar_voting_form
        }
    except Voting.DoesNotExist:
        raise Http404('Voting does not exist')
    return render(request, 'votings/votings_show.html', context)

def votings_edit(request, voting_id):
    voting = get_object_or_404(Voting, pk=voting_id)
    if request.method == "POST":
        form = VotingForm(request.POST, instance=voting)
        if form.is_valid():
            form.save()
    return redirect('votings:votings_show', voting_id=voting.id)

def votings_delete(request, voting_id):
    voting = get_object_or_404(Voting, pk=voting_id)
    assembly_id = voting.assembly.id
    if request.method == "POST":
        voting.delete()
    return redirect('votings:assemblies_show', assembly_id)

def votings_schedule(request, voting_id):
    voting = get_object_or_404(Voting, pk=voting_id)
    if request.method == "POST":
        form = VotingDatesForm(request.POST, instance=voting)
        if form.is_valid():
            form.save()
            voting.update_state()
            voting.save()
    return redirect('votings:votings_show', voting_id=voting.id)

def votings_unschedule(request, voting_id):
    voting = get_object_or_404(Voting, pk=voting_id)
    if request.method == "POST":
        voting.start_date = None
        voting.end_date = None
        voting.update_state()
        voting.save()
    return redirect('votings:votings_show', voting_id=voting.id)

def options_create(request, voting_id):
    voting = get_object_or_404(Voting, pk=voting_id)
    if request.method == "POST":
        form = OptionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.votes_quantity = 0
            option.voting = voting
            option.save()
    return redirect('votings:votings_show', voting_id=voting_id)

def options_edit(request, voting_id, option_id):
    option = get_object_or_404(Option, pk=option_id)
    if request.method == "POST":
        form = OptionForm(request.POST, instance=option)
        if form.is_valid():
            form.save()
    return redirect('votings:votings_show', voting_id=option.voting.id)

def options_delete(request, voting_id, option_id):
    option = get_object_or_404(Option, pk=option_id)
    if request.method == "POST":
        option.delete()
    return redirect('votings:votings_show', voting_id=option.voting.id)

def votes_create(request, voting_id, option_id):
    if request.method != "POST":
        raise Http404()
    option = get_object_or_404(Option, pk=option_id)
    voting = get_object_or_404(Voting, pk=voting_id)
    if option.voting.id != voting.id:
        raise Http404()
    if option.voting.state != VotingStates.ACTIVE:
        raise PermissionDenied()
    
    vote = Vote()
    participation = Participation()
    vote.option = option
    participation.user = request.user
    if not voting.are_votes_anonymous:
        vote.user = request.user
    vote.save()
    participation.save()
    return redirect('votings:votings_show', voting_id=option.voting.id)
