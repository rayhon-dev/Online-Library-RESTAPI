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

    def get_current_lending(self, obj):
        book_reservation = obj.book_reservations.filter(is_active=True).order_by('-reserved_at').first()
        if book_reservation:
            return {
                'id': book_reservation.id,
                'reserver': book_reservation.reserver.username,
                'expires_at': book_reservation.expires_at,
            }
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['book'] = BookShortSerializer(instance.book).data
        return data
