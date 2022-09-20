from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import MatchForm

from clubs.models import Result, Match, Round, Player, Club, PlayerScored


class StandingsView(View):
    def get(self, request):
        clubs = Result.objects.all().order_by('wins', 'draw')
        return render(request, 'filial.html', {'clubs': clubs})


class MatchView(View):
    def get(self, request):
        rounds = Round.objects.all().order_by('number')
        lis = []
        j = []
        for r in rounds:
            if r.matches.exists():
                for m in r.matches.all():
                    if not m.finish:
                        f = m
                        lis.append(f)
            if lis:
                j.append(lis)
                lis = []

        matches = Match.objects.filter(finish=False).order_by('-round')
        return render(request, 'match.html', {"matches": matches, 'rounds': rounds, 'm': j})


class SetResultView(View):
    def get(self, request, pk):
        try:
            match = Match.objects.filter(finish=False).get(pk=pk)
        except:
            raise ValueError({"error"" 'bunday o'yin yo'q"})
        form = MatchForm(instance=match)
        return render(request, 'set_result.html', {"form": form})

    def post(self, request, pk):
        match = Match.objects.get(pk=pk)
        form = MatchForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            club = form.cleaned_data['club1']
            club2 = form.cleaned_data['club2']
            print(f'{club} + {club2}')
            if Result.objects.filter(club=club).exists():
                result = Result.objects.filter(club=club).first()
                print(result)
                # result.math = match
                result.matches = result.matches + 1
                result.goals = result.goals + form.cleaned_data['club1_goals']
                result.missed = result.missed + form.cleaned_data['club2_goals']
                if form.cleaned_data['club1_goals'] > form.cleaned_data['club2_goals']:
                    result.wins = result.wins + 1
                elif form.cleaned_data['club1_goals'] < form.cleaned_data['club2_goals']:
                    result.lost = result.lost + 1
                else:
                    result.draw = result.draw + 1
                result.save()
            else:
                win=0
                lost=0
                draw=0
                if form.cleaned_data['club1_goals'] < form.cleaned_data['club2_goals']:
                    lost = lost + 1
                elif form.cleaned_data['club1_goals'] > form.cleaned_data['club2_goals']:
                    win = win + 1
                else:
                    draw = draw + 1
                new_result = Result.objects.create(
                    club=club, matches=1,
                    goals=form.cleaned_data['club1_goals'],
                    missed=form.cleaned_data['club2_goals'],
                    wins=win, draw=draw, lost=lost
                    )
            if Result.objects.filter(club=club2).exists():
                result = Result.objects.filter(club=club2).first()
                print(result.matches)
                # result.math = match
                result.matches = result.matches + 1
                print(result.matches)
                result.goals = result.goals + form.cleaned_data['club2_goals']
                result.missed = result.missed + form.cleaned_data['club1_goals']
                if form.cleaned_data['club1_goals'] < form.cleaned_data['club2_goals']:
                    result.wins = result.wins + 1
                elif form.cleaned_data['club1_goals'] > form.cleaned_data['club2_goals']:
                    result.lost = result.lost + 1
                else:
                    result.draw = result.draw + 1
                result.save()
            else:
                win = 0
                lost = 0
                draw = 0
                if form.cleaned_data['club1_goals'] > form.cleaned_data['club2_goals']:
                    lost = lost + 1
                elif form.cleaned_data['club1_goals'] < form.cleaned_data['club2_goals']:
                    win = win + 1
                else:
                    draw = draw + 1
                new_result = Result.objects.create(
                    club=club2, matches=1,
                    goals=form.cleaned_data['club2_goals'],
                    missed=form.cleaned_data['club1_goals'],
                    wins=win, draw=draw, lost=lost
                )
            return redirect('clubs:finished')
        else:
            return render(request, 'set_result.html', {"form": form})


class FinishedMatchView(View):
    def get(self, request):
        rounds = Round.objects.all().order_by('-number')
        lis = []
        j = []
        for r in rounds:
            if r.matches.exists():
                for m in r.matches.all():
                    if m.finish:
                        f = m
                        lis.append(f)
            if lis:
                j.append(lis)
                lis = []

        matches = Match.objects.filter(finish=True)
        return render(request, 'finished.html', {"matches": matches, 'rounds': rounds, 'm': j})


class ClubPlayers(View):
    def get(self, request, pk):
        club = Club.objects.get(pk=pk)
        players = Player.objects.filter(club__pk=pk)
        match_home = Match.objects.filter(Q(club1=club, finish=False) | Q(club2=club, finish=False)).order_by('round')[1:5]
        match_away = Match.objects.filter(Q(club1=club, finish=True) | Q(club2=club, finish=True)).order_by('-round')[1:5]
        return render(request, 'players.html', {"players": players, "club": club, 'match_n': match_home, 'match_l': match_away})



class TopScorer(View):
    def get(self, request):
        players = Player.objects.all().order_by('-goals')[0:5]
        return render(request, 'topurar.html', {"players": players})


class SetGoals(View):
    def get(self, request, pk):
        match = Match.objects.get(pk=pk)
        players = Player.objects.filter(Q(club=match.club1) | Q(club=match.club2))
        c = match.club1_goals
        l = []
        for a in range(0, c):
            l.append(a)
        return render(request, 'edit_goals.html', {"m": match, "c": l, "p": players})

    def post(self, request, pk):
        match = Match.objects.get(pk=pk)
        players = Player.objects.filter(Q(club=match.club1) | Q(club=match.club2))
        c = match.club1_goals + 1
        l = []
        print(request.POST)

        for a in range(1, c):
            a = str(a)
            x = request.POST[a]
            s = x.split()
            players = Player.objects.get(first_name=s[0], last_name=s[1])
            players.goals += 1
            players.save()
            match.goal_player.add(players)
            if PlayerScored.objects.filter(match=match, player=players).exists():
                new_player = PlayerScored.objects.get(
                    match=match,
                    player=players,
                )
                new_player.goals += 1
                new_player.save()
            else:
                PlayerScored.objects.create(
                    match=match,
                    player=players,
                    goals=1
                )

        return redirect(reverse('clubs:goals', kwargs={'pk': pk}))


class MatchDetail(View):
    def get(self, request, pk):
        match = Match.objects.get(pk=pk)

        return render(request, 'match_detail.html', {'m': match})
