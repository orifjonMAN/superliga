from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')
        write_only_field = {'password': 'write_only'}

    def save(self, **kwargs):
        email = self.validated_data['email']
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        password = self.validated_data['password']

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'this email already exists'})
        account = User(username=username,
                       email=email,
                       first_name=first_name,
                       last_name=last_name)
        account.set_password(password)
        account.save()
        return account


# class UserLoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', 'password')
#         write_only_field = {'password': 'write_only'}
#
#     def validate(self, data):
#         password = data['password']
#         username = data['username']
#
#         if User.objects.get(username=username).exists():
#             if not
#             check_password(password, password):
#                 raise ValidationError({'error': 'your password doesn\'t match for your username' })
#             acc = User.objects.get(username=username)
#             # acc.is_valid()
#             return acc
#         else:
#             raise ValidationError({'error': 'incorrect username'})
