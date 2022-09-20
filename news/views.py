from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from news.models import New, Review


class NewsDetail(View):
    def get(self, request, slug):
        new = get_object_or_404(New, slug=slug)
        new.views += 1
        new.save()
        id = new.id
        new_tags_ids = new.tags.values_list('id', flat=True)
        similar_posts = New.objects.filter(tags__in=new_tags_ids).exclude(id=id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created')[:4]

        return render(request, 'single.html', {'new': new, 's_post': similar_posts})


class CreateReview(LoginRequiredMixin, View):
    def post(self, request, slug):
        if request.method == 'POST':
            new = get_object_or_404(New, slug=slug)
            comment = request.POST['message']
            new_comment = Review.objects.create(
                user=request.user,
                new=new,
                comment=comment
            )
        return redirect(reverse('new:detail', kwargs={'slug': slug}))


class CreateReplyView(LoginRequiredMixin, View):
    def get(self, request, id, slug):
        new = get_object_or_404(New, slug=slug)
        review = get_object_or_404(Review, id=id)
        ctx = {
            'new': new,
            'review': review,
        }
        return render(request, 'review.html', ctx)

    def post(self, request, id, slug):
        new = get_object_or_404(New, slug=slug)
        review = get_object_or_404(Review, id=id)
        reply_user = review.user
        if request.method == 'POST':
            comment = request.POST['comment']
            new_comment = Review.objects.create(
                new=new,
                user=request.user,
                reply=review,
                comment=comment
            )
            return redirect(reverse('new:detail', args=[slug]))
        else:
            return render(request, 'review.html')

