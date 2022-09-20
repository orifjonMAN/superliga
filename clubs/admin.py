from django.contrib import admin
from .models import Club, Player, Match, Result, Round, PlayerScored

admin.site.register(Club)
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(Result)
admin.site.register(Round)
admin.site.register(PlayerScored)
# Register your models here.
