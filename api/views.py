from django.shortcuts import get_object_or_404
from rest_framework import status, views
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer


class BookListCreateAPIView(views.APIView):
    """  hand book list and create it by API class """

    def get(self, request, *args, **kwargs):
        """ the handler method get the Book-model """

        # get a list of model object
        book_list = Book.objects.all()

        # make instance of BooKSerializer
        serializer = BookSerializer(instance=book_list, many=True)

        # return response object
        return Response(serializer.data, status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        """ tha handler method register book model """

        serializer = BookSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class BookRetrieveUpdateDestroyAPIView(views.APIView):
    """ the class hands book-detail, update a book, delete a book by API """

    def get(self, request, pk, *args, **kwargs):
        """ the handler does a detail of book """

        # get the model object
        book = get_object_or_404(Book, pk=pk)

        # made an instance of serializer
        serializer = BookSerializer(instance=book)

        # return a response object
        return Response(serializer.data, status.HTTP_200_OK)


    def put(self, request, pk, *args, **kwargs):
        """ update book by api """

        # get an object of model
        book = get_object_or_404(Book, pk=pk)

        # make an instance of serializer
        serializer = BookSerializer(instance=book, data=request.data)

        # do validation
        serializer.is_valid(raise_exception=True)

        # update the book
        serializer.save()

        # return response object
        return Response(serializer.data, status.HTTP_200_OK)


    def patch(self, request, pk, *args, **kwargs):
        """ update a part of book model by api """

        book = get_object_or_404(Book, pk=pk)

        serializer = BookSerializer(instance=book, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)


    def delete(self, request, pk, *args, **kwargs):
        """ delete a book model by api """

        book = get_object_or_404(Book, pk=pk)

        book.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
