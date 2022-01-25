from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic
from .models import Option, Voting, VotingStates
from .forms import OptionForm, VotingForm

def votings_index(request):
    voting_list = Voting.objects.all()
    context = {
        'voting_list':voting_list,
    }
    return render(request, 'votings/votings_index.html', context)

def votings_create(request):
    if request.method == "POST":
        form = VotingForm(request.POST)
        if form.is_valid():
            voting = form.save(commit=False)
            voting.electorate_quantity = 0
            voting.votes_quantity = 0
            voting.state = VotingStates.EDITABLE
            voting.save()
            return redirect('votings:votings_show', voting_id=voting.id)
    else:
        form = VotingForm()
    return render(request, 'votings/votings_create.html', {'form': form})

def votings_show(request, voting_id):
    try:
        voting:Voting = Voting.objects.get(pk=voting_id)
        options = voting.option_set.all()
        form = OptionForm()
        context = {
            'voting':voting,
            'options':options,
            'form':form,
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
    else:
        form = VotingForm(instance=voting)
    return render(request, 'votings/votings_edit.html', {'form': form})

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

def options(request, voting_id):
    if request.method == 'POST':
        voting = Voting.objects.get(pk=voting_id)
        new_option = Option(index_number=1, title_text=request.POST['answer'], voting=voting)
        new_option.save()
        #options_list = Option.objects.filter(voting_id=voting_id)
        #return render(request, 'votings/option.html', {'options_list':options_list, 'voting_id':voting_id})
        return HttpResponseRedirect(reverse('votings:options', args=(voting.id,)))
    else:
        options_list = Option.objects.filter(voting_id=voting_id)
        return render(request, 'votings/options.html', {'options_list':options_list, 'voting_id':voting_id})