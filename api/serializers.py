from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from clubs.models import Club, Player, Match, Result


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('id', 'date', 'club1', 'club2', 'match_type')
        read_only_fields = ('club1_goals', 'club2_goals', 'lineups', 'finish')

    def validate(self, data):
        if data['club1'] == data['club2']:
            raise ValidationError('clubs should be different')
        else:
            return data


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('first_name', 'last_name', 'position', 'birth_date', 'club')


class ClubSerializer(serializers.ModelSerializer):
    players = serializers.StringRelatedField(many=True, read_only=True)
    home_match = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='api:detail'
    )
    away_match = serializers.StringRelatedField(many=True, read_only=True)
    results = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Club
        fields = ('id', 'name', 'city', 'stadium', 'players', 'home_match', 'away_match', 'results')


class MatchFinishSerializer(serializers.ModelSerializer):
    club1 = ClubSerializer(read_only=True)
    club2 = ClubSerializer(read_only=True)

    class Meta:
        model = Match
        fields = ('id', 'date', 'finish', 'club1_goals', 'club2_goals', 'club1', 'club2', 'match_type')


class ResultSerializer(serializers.ModelSerializer):
    match = MatchSerializer(read_only=True)
    club = ClubSerializer(read_only=True)

    class Meta:
        model = Result
        fields = ('club', 'match', 'matches', 'wins', 'draw', 'lost', 'goals', 'missed')
