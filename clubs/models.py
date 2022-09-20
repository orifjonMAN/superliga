from django.db import models
from rest_framework.exceptions import ValidationError


class Round(models.Model):
    number = models.IntegerField(default=0, unique=True)

    def __str__(self):
        return str(self.number)


class Club(models.Model):
    name = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=20)
    stadium = models.CharField(max_length=25, blank=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    position = (
        ('Goalkeeper', 'goalkeeper'),
        ('Midfielder', "midfielder"),
        ('Defender', 'defender'),
        ('Forward', 'forward')
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=15, choices=position, default='Forward')
    birth_date = models.DateField()
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='players')
    goals = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Match(models.Model):
    match_type = (
        ('Superliga', 'Superliga'),
        ('Kubok', 'Kubok'),
    )
    date = models.DateField()
    club1 = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='home_match')
    club2 = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='away_match')
    lineups = models.TextField(blank=True)
    match_type = models.CharField(max_length=15, choices=match_type, default='Superliga')
    club1_goals = models.IntegerField(default=0)
    club2_goals = models.IntegerField(default=0)
    finish = models.BooleanField(default=False)
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='matches')
    goal_player = models.ManyToManyField(Player, blank=True)

    def __str__(self):
        return "%s: %s %s:%s  %s. %s , %s" % (
            self.match_type,
            self.club1.name,
            self.club1_goals,
            self.club2_goals,
            self.club2.name,
            self.date,
            self.finish
        )


class PlayerScored(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='scored')
    goals = models.IntegerField(default=0)

    def __str__(self):
        return self.player.first_name


class Result(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='results')
    matches = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draw = models.IntegerField(default=0)
    lost = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)
    missed = models.IntegerField(default=0)

    def __str__(self):
        return '%s : matches-%s, wins-%s, T/N-%s:%s' % (
            self.club.name,
            self.matches,
            self.wins,
            self.goals,
            self.missed
        )

    def get_score(self):
        score = 3 * self.wins + self.draw
        return score
