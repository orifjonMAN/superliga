import json

from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (ClubSerializer,
                          PlayerSerializer,
                          MatchSerializer,
                          ResultSerializer,
                          MatchFinishSerializer,
                          )
from clubs.models import Club, Player, Match, Result
from .user_serializer import UserSerializer


class UserRegisterAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'Successfully registration'
            data['username'] = account.username
            data['email'] = account.email
            data['first_name'] = account.first_name
            data['last_name'] = account.last_name

            token = Token.objects.create(user=account).key
            data['token'] = token
            return Response(data=data)
        else:
            return Response(data=serializer.errors)


class UserLoginAPIView(APIView):
    def put(self, request):
        data = {}
        # bod = request.data
        # bod1 = json.dumps(bod)
        body = json.loads(json.dumps(request.data))
        username = body['username']
        password = body['password']
        try:
            acc = User.objects.get(username=username)
        except:
            ValidationError({'error': 'error boldi'})

        token = Token.objects.get(user=acc).key
        if not check_password(password, acc.password):
            raise ValidationError({'error': 'password is not matching correctly'})
        if acc:
            if acc.is_active:
                login(request, acc)
                data['message'] = 'you are logged in'
                data['username'] = acc.username
                data['token'] = token
                return Response(data=data)
            else:
                raise ValidationError({'error': 'account is not active'})
        else:
            raise ValidationError({'error': "no account"})


# class ExampleView(APIView):
#     def get(self, request, format=None):
#         content = {
#             'user': str(request.user),  # `django.contrib.auth.User` instance.
#             'auth': str(request.auth),  # None
#         }
#         return Response(content)
#
#     def post(self, request):
#         pass


class ClubListAPIView(APIView):
    def get(self, request):
        clubs = Club.objects.all()
        # permission =
        serializer = ClubSerializer(clubs, many=True, context={'request': request})
        return Response(data=serializer.data)

    def post(self, request):
        # clubs = Club.objects.all()
        serializer = ClubSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class PlayerListAPIView(APIView):
    def get(self, request):
        clubs = Player.objects.all()
        serializer = PlayerSerializer(clubs, many=True)
        return Response(data=serializer.data)

    def post(self, request):
        # clubs = Club.objects.all()
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class MatchListAPIView(APIView):
    def get(self, request):
        clubs = Match.objects.filter(finish=False)
        serializer = MatchSerializer(clubs, many=True)
        return Response(data=serializer.data)

    def post(self, request):
        # clubs = Club.objects.all()
        serializer = MatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class MatchDetailAPIView(APIView):
    def get(self, request, pk):
        match = Match.objects.get(pk=pk)
        serializer = MatchFinishSerializer(match,
                                           context={'request': request})
        return Response(data=serializer.data)

    def patch(self, request, pk):
        match = Match.objects.get(pk=pk)
        serializer = MatchFinishSerializer(match, data=request.data,
                                           context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
        result = Result.objects.create(club=match.club1, match=match,
                                       goals=match.club1_goals,
                                       missed=match.club2_goals, matches=1, )
        # serializer1 = ResultSerializer(data=result, context={'request': request})
        # if serializer1.is_valid():
        #     serializer1.save()
        result2 = Result.objects.create(club=match.club2, match=match,
                                        goals=match.club2_goals,
                                        missed=match.club1_goals, matches=1, )
        # serializer2 = ResultSerializer(data=result2, context={'request': request})
        # if serializer2.is_valid():
        #     serializer2.save()
        return Response(data=serializer.data)


class MatchFinishAPIView(ListAPIView):
    queryset = Match.objects.filter(finish=True)
    serializer_class = MatchFinishSerializer


class ResultListAPIView(APIView):
    def get(self, request):
        result = Result.objects.all()
        serializer = ResultSerializer(result, many=True, context={'request': request})
        return Response(data=serializer.data)
