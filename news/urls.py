from django.urls import path
from news.views import NewsDetail, CreateReview, CreateReplyView

app_name = 'new'
urlpatterns = [
    path('<slug:slug>/', NewsDetail.as_view(), name='detail'),
    path('create_comment/<slug:slug>', CreateReview.as_view(), name='create_comment'),
    path('create_reply/<int:id>/<slug:slug>', CreateReplyView.as_view(), name='create_reply'),
]
