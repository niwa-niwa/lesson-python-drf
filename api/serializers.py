from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """ the serializer for Book-Model """

    class Meta:

        # select the Model-class
        model = Book

        # select fields that are exclude useing the serializer
        exclude = ['created_at']
