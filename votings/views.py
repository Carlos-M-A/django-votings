from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.exceptions import PermissionDenied, BadRequest
from django.db.models import Q
from .models import Assembly, Membership, Option, Organization, Participation, Vote, Voting, VotingStates
from .forms import OptionForm, SearchVotingForm, VotingDatesForm, VotingForm, SearchMemberForm, SearchVotesForm
from django.contrib.auth.models import User

def organizations_show(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)
    assemblies = organization.assembly_set.all()
    data = {'id_organization':organization.id}
    search_voting_form = SearchVotingForm(initial=data)
    context = {
        'organization':organization,
        'assemblies':assemblies,
        'search_voting_form':search_voting_form,
    }
    return render(request, 'votings/organization_show.html', context)

def organization_create(request):
    pass

def assemblies_show(request, assembly_id):
    assembly = get_object_or_404(Assembly, pk=assembly_id)
    voting = Voting()
    voting.assembly = assembly
    new_voting_form = VotingForm(instance=voting)
    data = {'id_assembly':assembly.id}
    search_voting_form = SearchVotingForm(initial=data)
    search_member_form = SearchMemberForm(initial=data)
    planned_votings = assembly.voting_set.filter(state=VotingStates.PLANNED)
    scheduled_votings = assembly.voting_set.filter(state=VotingStates.SCHEDULED).order_by('start_date')
    active_votings = assembly.voting_set.filter(state=VotingStates.ACTIVE)
    finished_votings = assembly.voting_set.filter(state=VotingStates.FINISHED).order_by('-start_date')
    context = {
        'assembly':assembly,
        'new_voting_form':new_voting_form,
        'search_voting_form':search_voting_form,
        'search_member_form':search_member_form,
        'planned_votings':planned_votings,
        'scheduled_votings':scheduled_votings,
        'active_votings':active_votings,
        'finished_votings':finished_votings,
    }
    return render(request, 'votings/assemblies_show.html', context)

def members_search(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)
    form = SearchMemberForm(request.GET)
    if form.is_valid():
        text = form.cleaned_data['text']
        date = form.cleaned_data['date']
        id_assembly = form.cleaned_data['id_assembly']

    membership_list = Membership.objects.filter(assembly__organization=organization)
    if id_assembly != None:
        assembly = get_object_or_404(Assembly, pk=int(id_assembly))
        membership_list = membership_list.filter(assembly=assembly)
    else:
        membership_list = membership_list.filter(assembly=organization.general_assembly)
    
    membership_list = membership_list.filter(Q(user__username__icontains=text) | Q(user__first_name__icontains=text) | Q(user__last_name__icontains=text))
    if date != None:
        membership_list = membership_list.filter(start_date__lte=date)
        membership_list = membership_list.exclude(end_date__lte=date)
    else:
        membership_list = membership_list.filter(end_date=None)

    context = {
            'form':form,
            'organization':organization,
            'membership_list':membership_list,
        }
    return render(request, 'votings/members_search.html', context)

def users_search(request, assembly_id):
    pass

def votings_search(request):
    form = SearchVotingForm(request.GET)
    if form.is_valid():
        text = form.cleaned_data['text']
        state = form.cleaned_data['state']
        date_since = form.cleaned_data['date_since']
        date_until = form.cleaned_data['date_until']
        id_assembly = form.cleaned_data['id_assembly']
        id_organization = form.cleaned_data['id_organization']

        voting_list = Voting.objects.filter(Q(title_text__icontains=text) | Q(question_text__icontains=text))
        if id_assembly != None:
            assembly = get_object_or_404(Assembly, pk=int(id_assembly))
            voting_list = voting_list.filter(assembly=assembly)
        if id_organization != None:
            organization = get_object_or_404(Organization, pk=int(id_organization))
            voting_list = voting_list.filter(assembly__in=organization.assembly_set.all())
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

def votings_create(request):
    if request.method == "POST":
        form = VotingForm(request.POST)
        if form.is_valid():
            voting = form.save(commit=False)
            voting.electorate_quantity = 0
            voting.votes_quantity = 0
            voting.state = VotingStates.PLANNED
            voting.save()
            return redirect('votings:votings_show', voting_id=voting.id)
        else:
            raise BadRequest()
    else:
        raise BadRequest()

def votings_show_finished_voting(request, voting, options):
    context = {
            'voting':voting,
            'options':options,
        }
    return render(request, 'votings/finished_voting_show.html', context)

def votings_show(request, voting_id):
    try:
        voting:Voting = Voting.objects.get(pk=voting_id)
        options = voting.option_set.all()
        if voting.state == VotingStates.FINISHED:
            return votings_show_finished_voting(request, voting, options)
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
    if not voting.are_votes_anonymous:
        vote.user = request.user
    vote.option = option
    vote.save()
    participation = Participation()
    participation.user = request.user
    participation.voting = voting
    participation.participation_check = True
    participation.save()

    context = {
        'voting':voting,
        'option':option,
        'vote':vote
    }
    return render(request, 'votings/cast_vote_show.html', context)

def votes_search(request, voting_id):
    voting = get_object_or_404(Voting, pk=voting_id)
    form = SearchVotesForm(request.GET)
    if form.is_valid():
        registration_number = form.cleaned_data['registration_number']
        index_number = form.cleaned_data['index_number']
        username = form.cleaned_data['username']

    votes_list = Vote.objects.filter(option__voting=voting)
    if index_number != None:
        votes_list = votes_list.filter(option__index_number=index_number)
    if registration_number != None:
        votes_list = votes_list.filter(id=registration_number)
    if username != None and len(username) > 0:
        votes_list = votes_list.filter(Q(user__username__icontains=username) | Q(user__first_name__icontains=username) | Q(user__last_name__icontains=username))

    context = {
        'voting':voting,
        'search_votes_form':form,
        'votes_list':votes_list
    }
    return render(request, 'votings/votes_search.html', context)
