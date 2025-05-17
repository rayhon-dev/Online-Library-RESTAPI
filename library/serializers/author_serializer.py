from rest_framework import serializers
from library.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'id',
            'first_name',
            'last_name',
            'bio',
            'birth_date',
            'nationality'
        ]