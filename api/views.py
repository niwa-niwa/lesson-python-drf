from django.shortcuts import get_object_or_404
from rest_framework import status, views
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError

from .models import Book
from .serializers import BookSerializer


class BookDestroyAPIView(views.APIView):
    """ 本モデルの削除APIクラス """
    def delete(self, request, pk, *args, **kwargs):
        # モデルオブジェクトを取得
        book = get_object_or_404(Book, pk=pk)
        # モデルオブジェクトを削除
        book.delete()
        # レスポンスオブジェクトを作成して返す
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookUpdateAPIView(views.APIView):
    """ 本モデルの更新・一部更新APIクラス """
    def put(self, request, pk, *args, **kwargs):
        # モデルオブジェクト取得
        book = get_object_or_404(Book, pk=pk)
        # シリアライザーオブジェクト作成
        serializer = BookSerializer(instance=book, data=request.data)
        # バリデーションを実行
        serializer.is_valid(raise_exception=True)
        # モデルオブジェクトを更新
        serializer.save()
        # レスポンスオブジェクトを作成して返す
        return Response(serializer.data, status_HTTP_200_OK)

    def patch(self, request, pk, *args, **kwargs):
        """ 本モデルの一部更新 """
        # モデルオブジェクトを取得
        serializer = BookSerializer(instance=book, data=request.data, partial=True)
        # バリデーションを実行
        serializer.is_valid(raise_exception=True)
        # モデルオブジェクトを一部更新
        serializer.save()
        # レスポンスオブジェクトを作成して返す
        return Response(serializer.data, status.HTTP_200_OK)


class BookRetrieveAPIView(views.APIView):
    """ 本モデルの取得(詳細)APIクラス """

    def get(self, request, pk, *args, **kwargs):
        # モデルオブジェクトを取得
        book = get_object_or_404(Book, pk=pk)
        # シリアライザーオブジェクトを作成
        serializer = BookSerializer(instance=book)
        # レスポンスオブジェクトを作成して返す
        return Response(serializer.data, status.HTTP_200_OK)


class BookFilter(filters.FilterSet):
    """ 本モデル用フィルタクラス """

    class Meta:
        model = Book
        fields = "__all__"


class BookListAPIView(views.APIView):
    """ 本モデルの取得(一覧)APIに対応するハンドラメソッド """

    def get(self, request, *args, **kwargs):

        # モデルオブジェクトをクエリ文字列を使ってフィルタリングした結果を取得
        filterset = BookFilter(request.query_params, queryset=Book.objects.all())
        if not filterset.is_valid():
            # クエリ文字列のバリデーションがNGの場合は400エラー
            raise ValidationError(filterset.errors)

        # シリアライザーオブジェクトを作成
        serializer = BookSerializer(instance=filterset.qs, many=True)

        # レスポンスオブジェクトを作成して返す
        return Response(serializer.data, status.HTTP_200_OK)


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
