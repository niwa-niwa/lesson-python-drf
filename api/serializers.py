import random
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Book
from django.utils import timezone
from django.core.validators import RegexValidator


class BookSerializer(serializers.ModelSerializer):
    """ the serializer for Book-Model """

    # priceを文字列に変更
    # price = serializers.CharField(read_only=True)

    class Meta:

        # select the Model-class
        model = Book

        # シリアライズするフィールド fieldsかexcludeをどちらかしか利用できない
        # fields = ['id', 'title', 'price']

        # select fields that are exclude useing the serializer
        exclude = ['created_at']

        validators = [
            # タイトルと価格でユニークになっていることを検証
            UniqueTogetherValidator(
                queryset=Book.objects.all(),
                fields=('title', 'price'),
                message="タイトルと価格でユニークになっていなければいけません。"
            ),
        ]

        extra_kwargs = {
            'title' : {
                'error_messages':{
                    'blank':"タイトルは必須です。",
                },
                'validators': [
                    RegexValidator(r'D.+$', message="タイトル「D」で始めてください。"),
                ],
            },
            'price':{
                'error_messages':{
                    'invalid':"価格には整数の値を入力してください。"
                },
            },
        }

    def validate_title(self, value):
        """ タイトルに対するバリデーションメソッド """
        if 'Java' in value:
            raise serializers.ValidationError(
        "タイトルには「Java」を含めないでください。")
        return value

    def validate(self, data):
        """ 複数フィールド間のバリデーションメソッド """
        title = data.get('title')
        price = data.get('price')
        if title and '薄い本' in title and price and price > 3000:
            raise serializers.ValidationError("薄い本は3,000円を超えてはいけません。")
        return data


# サンプル
class BookListSerializer(serializers.ListSerializer):
    """ 複数の本モデルをまとめてうためのシリアライザー """

    # 対象のシリアライザを指定
    child = BookSerializer()


# サンプル
class FortuneSerializer(serializers.Serializer):
    """ 今日の運勢を返すシリアライザー モデルには依存しない """

    birth_data = serializers.DateField()
    blood_type = serializers.ChoiceField(choices=['A', 'B', 'O', 'AB'])

    # 出力時に get_current_date() が呼ばれる
    current_date = serializers.SerializerMethodField()

    # 出力時に get_fortune() が呼ばれる
    fourtune = serializers.SerializerMethodField()

    def get_current_date(self, obj):
        return timezone.localdate()

    def get_fortune(self, obj):
        seed = '{}{}{}'.format(
            timezone.localdate(), obj['birth_date'], obj['blood_type']
        )
        random.seed(seed)
        return random.choice(
            ['★☆☆☆☆', '★★☆☆☆', '★★★☆☆', '★★★★☆', '★★★★★',]
        )
"""
POSTで渡すJSON
{
    "birth_date": "1990-01-01"
    "blood_type": "A"
}

返されるJSON
{
    "birth_date":"1990-01-01",
    "blood_type":"A",
    "current_date":"2019-09-22",
    "fortune":"★★★★☆"
}
"""