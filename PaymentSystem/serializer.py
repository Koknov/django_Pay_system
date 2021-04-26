from rest_framework import serializers

from PaymentSystem.models import Transaction, Users


class UsersSerializer(serializers.ModelSerializer):
    """
    Serializing all the users
    """

    class Meta:
        model = Users
        fields = ('wallet_number', 'username', 'total', 'token')
        read_only_fields = ('wallet_number',)


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializing all the transactions
    """

    class Meta:
        model = Transaction
        fields = ('sender_wallet_number', 'receiver_wallet_number', 'transaction_amount')


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Users
        fields = ['username', 'wallet_number', 'password', 'token']
        read_only_fields = ('wallet_number',)

    def create(self, validated_data):
        return Users.objects.create_user(**validated_data)
