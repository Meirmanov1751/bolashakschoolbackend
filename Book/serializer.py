from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from .models import Book, BookImages


class BookImageSerializer(ModelSerializer):
    class Meta:
        model = BookImages
        fields = '__all__'

class BookSerializer(ModelSerializer):
    images = BookImageSerializer(many=True)

    class Meta:
        model = Book
        fields = '__all__'
