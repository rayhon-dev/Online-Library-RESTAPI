from rest_framework import serializers
from library.models import Rating, Book

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    book = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Book.objects.all())

    class Meta:
        model = Rating
        fields = ['id', 'user', 'book', 'rating', 'review']
