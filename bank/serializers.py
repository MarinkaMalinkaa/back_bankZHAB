from bank.models import AuthUser, Account, Card, Contract, Status, Transaction
from rest_framework import serializers
from django_filters import rest_framework as filters



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = AuthUser
        # Поля, которые мы сериализуем
        fields = ["pk",  "password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined", "phone"]


class UserFilter(filters.FilterSet):
    pass
    search = filters.CharFilter(field_name='last_name')

    class Meta:
        model = AuthUser
        fields = ["last_name"]

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Account
        # Поля, которые мы сериализуем
        fields = ["pk",  "authuser", "account_num", "balance"]


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Card
        # Поля, которые мы сериализуем
        fields = ["pk",  "number_card", "cvc", "pin", "contract"]


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Contract
        # Поля, которые мы сериализуем
        fields = ["pk",  "status", "account", "auth_user"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Transaction
        # Поля, которые мы сериализуем
        fields = ["pk",  "sum_transaction", "account1", "account2"]


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Status
        # Поля, которые мы сериализуем
        fields = ["pk",  "flag"]





