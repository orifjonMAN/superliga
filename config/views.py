from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views import View
from news.models import New
# from team.models import Coach
from news.new_tags import get_most_commented_posts


class Home(View):
    def get(self, request):
        q = None
        # coaches = Coach.objects.all()
        news = New.objects.all().order_by('-created')
        if request.GET.get('q'):
            q = request.GET.get('q')
            news = news.filter(
                               Q(title__icontains=q),
                               # Q(body__search__icontains=q),
                               # Q(body1__search__icontains=q),
                               # Q(body2__search__icontains=q),
                               )
        else:
            news = news.all()
        # three_news = news[:2]
        paginator = Paginator(news, 6)
        page = request.GET.get('page', 1)

        news = paginator.page(page)

        ctx = {
            # 'three_news': three_news,
            'last_three_news': news,
            # 'coaches': coaches,
            'get_most_commented_posts': get_most_commented_posts
        }
        return render(request, 'index.html', ctx)


