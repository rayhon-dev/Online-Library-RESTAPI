from rest_framework import serializers
from library.models import BookCopy


class BookShortSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    isbn = serializers.CharField(read_only=True)


class BookCopySerializer(serializers.ModelSerializer):
    current_lending = serializers.SerializerMethodField()

    class Meta:
        model = BookCopy
        fields = [
            'id',
            'book',
            'inventory_number',
            'condition',
            'is_available',
            'added_date',
            'current_lending'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['book'] = BookShortSerializer(instance.book).data
        return data
