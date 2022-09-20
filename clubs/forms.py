from django import forms
from .models import Match


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('match_type', 'club1', 'club1_goals', 'club2', 'club2_goals', 'date', 'finish')
