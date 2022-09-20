from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View


class SignupView(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        if request.method == 'POST':
            cd = request.POST
            username = cd['username']
            email = cd['email']
            name = cd['name']
            password = cd['password']
            last_name = cd['familiya']
            if not User.objects.filter(username=username):
                new_user = User.objects.create_user(
                    username=username,
                    first_name=name,
                    last_name=last_name,
                    email=email,
                    password=password
                )
                login(request, new_user)
                messages.info(request, 'You are successfully signed up')
                return redirect('home')
            else:
                messages.info(request, 'bu username oldin ro\'yhatdan o\'tgan')
                return render(request, 'signup.html')


class Logout(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        logout(request)
        return redirect('home')


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        if request.method == 'POST':
            username=request.POST['username']
            password=request.POST['password']

            if User.objects.filter(username=username):
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.info(request, 'password is not correct')
                    return render(request, 'login.html')
            else:
                messages.info(request, 'username is not correct')
                return render(request, 'login.html')
