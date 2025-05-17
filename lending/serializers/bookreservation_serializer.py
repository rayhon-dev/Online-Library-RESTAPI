from rest_framework import serializers
from lending.models import BookReservation
from users.models import CustomUser


class BookCopyShortSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    inventory_number = serializers.CharField(read_only=True)

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name']

class BookReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReservation
        fields = [
            'id',
            'book_copy',
            'reserver',
            'reserved_at',
            'expires_at',
            'is_active',
        ]


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['book_copy'] = BookCopyShortSerializer(instance.book_copy).data
        data['reserver'] = UserShortSerializer(instance.reserver).data
        return data