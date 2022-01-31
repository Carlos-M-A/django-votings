from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic
from .models import Assembly, Option, Voting, VotingStates
from .forms import OptionForm, VotingDatesForm, VotingForm

def general_index(request, general_assembly_id):
    general_assembly = get_object_or_404(Assembly, pk=general_assembly_id)
    assemblies = general_assembly.assembly_set.all()
    context = {
        'general_assembly':general_assembly,
        'assemblies':assemblies
    }
    return render(request, 'votings/general_index.html', context)

def assemblies_show(request, assembly_id):
    assembly = get_object_or_404(Assembly, pk=assembly_id)
    new_voting_form = VotingForm()
    context = {
        'assembly':assembly,
        'new_voting_form':new_voting_form
    }
    return render(request, 'votings/assemblies_show.html', context)

def votings_index(request):
    voting_list = Voting.objects.all()
    context = {
        'voting_list':voting_list,
    }
    return render(request, 'votings/votings_index.html', context)

def votings_create(request, assembly_id):
    assembly = get_object_or_404(Assembly, pk=assembly_id)
    if request.method == "POST":
        form = VotingForm(request.POST)
        if form.is_valid():
            voting = form.save(commit=False)
            voting.assembly = assembly
            voting.electorate_quantity = 0
            voting.votes_quantity = 0
            voting.state = VotingStates.EDITABLE
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
        calendar_voting_form = VotingDatesForm()
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

def votings_calendar(request, voting_id):
    voting = get_object_or_404(Voting, pk=voting_id)
    if request.method == "POST":
        form = VotingForm(request.POST, instance=voting)
        if form.is_valid():
            form.save()
    return redirect('votings:votings_show', voting_id=voting.id)

def votings_delete(request, voting_id):
    voting = get_object_or_404(Voting, pk=voting_id)
    if request.method == "POST":
        voting.delete()
        return redirect('votings:votings_index')
    else:
        form = VotingForm(instance=voting)
    return render(request, 'votings/votings_delete.html', {'voting': voting})

def options_create(request, voting_id):
    voting = get_object_or_404(Voting, pk=voting_id)
    form = OptionForm(request.POST)
    if form.is_valid():
        option = form.save(commit=False)
        option.votes_quantity = 0
        option.voting = voting
        option.save()
    return redirect('votings:votings_show', voting_id=voting_id)

def options_edit(request, voting_id, option_id):
    option = get_object_or_404(Option, pk=option_id)
    form = OptionForm(request.POST, instance=option)
    if form.is_valid():
        form.save()
    return redirect('votings:votings_show', voting_id=option.voting.id)

def options_delete(request, voting_id, option_id):
    option = get_object_or_404(Option, pk=option_id)
    option.delete()
    return redirect('votings:votings_show', voting_id=option.voting.id)