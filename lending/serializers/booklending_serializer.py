from rest_framework import serializers
from lending.models import BookLending, BookReservation


class BookCopyShortSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    inventory_number = serializers.CharField(read_only=True)


class BookLendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookLending
        fields = [
            'id',
            'book_copy',
            'borrower',
            'borrowed_date',
            'due_date',
            'returned_date',
            'status'
        ]


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['book_copy'] = BookCopyShortSerializer(instance.book_copy).data
        return data