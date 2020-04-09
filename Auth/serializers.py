from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from .models import MyUser, AnalyticsChild


class UserWriteSerializer(ModelSerializer):
    def create(self, validated_data):
        print(validated_data)
        password = validated_data.pop('password', None)
        print(password)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = MyUser
        exclude = ('is_admin', 'is_active')


class UserReadSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        exclude = ('password', 'is_admin', 'is_active')


class AnalyticsChildSerializer(ModelSerializer):
    class Meta:
        model = AnalyticsChild
        fields = '__all__'

class LoginSerializer(Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
