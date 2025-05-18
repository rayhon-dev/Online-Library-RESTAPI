from rest_framework import serializers
from library.models import Book



class BookAuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)


class BookGenreSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)


class BookSerializer(serializers.ModelSerializer):
    copies_available = serializers.SerializerMethodField()
    authors = BookAuthorSerializer(many=True, read_only=True)  # Nested serializer
    genre = BookGenreSerializer(read_only=True)  # Nested serializer

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'authors', 'genre', 'isbn', 'published_date',
            'description', 'page_count', 'language', 'copies_available'
        ]

    def get_copies_available(self, obj):
        if hasattr(obj, 'copies_count'):
            return obj.copies_count
        return obj.book_copies.count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['authors'] = BookAuthorSerializer(instance.authors.all(), many=True).data
        data['genre'] = BookGenreSerializer(instance.genre).data
        return data


class AuthorBookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    isbn = serializers.CharField(read_only=True)
    published_date = serializers.DateField(read_only=True)
    copies_available = serializers.IntegerField(read_only=True)


