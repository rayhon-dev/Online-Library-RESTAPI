from rest_framework import serializers
from library.models import Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = [
            'id',
            'name',
            'description'
        ]