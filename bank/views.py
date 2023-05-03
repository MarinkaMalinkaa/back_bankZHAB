from random import randint

from rest_framework import viewsets
from bank.serializers import UserSerializer, UserFilter, AccountSerializer, CardSerializer, ContractSerializer, \
    TransactionSerializer, StatusSerializer
from bank.models import AuthUser, Account, Card, Contract, Transaction, Status
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
import redis
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import uuid


session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


class UserViewSet(viewsets.ModelViewSet):
    # Описание класса пользователей, добавляем тут сериалайзер и поля для фильтрации
    # queryset всех пользователей для фильтрации по дате последнего изменения
    queryset = AuthUser.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilter
    search_fields = ['^last_name']


class AccountViewSet(viewsets.ModelViewSet):
    # Описание класса пользователей, добавляем тут сериалайзер и поля для фильтрации
    # queryset всех пользователей для фильтрации по дате последнего изменения
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class CardViewSet(viewsets.ModelViewSet):
    # Описание класса пользователей, добавляем тут сериалайзер и поля для фильтрации
    # queryset всех пользователей для фильтрации по дате последнего изменения
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class ContractViewSet(viewsets.ModelViewSet):
    # Описание класса пользователей, добавляем тут сериалайзер и поля для фильтрации
    # queryset всех пользователей для фильтрации по дате последнего изменения
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    # Описание класса пользователей, добавляем тут сериалайзер и поля для фильтрации
    # queryset всех пользователей для фильтрации по дате последнего изменения
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class StatusViewSet(viewsets.ModelViewSet):
    # Описание класса пользователей, добавляем тут сериалайзер и поля для фильтрации
    # queryset всех пользователей для фильтрации по дате последнего изменения
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


def GetRandomCard():
    random_num_card = randint(2023000000000000, 2023999999999999)

    uniqe_confirm = Card.objects.filter(number_card=random_num_card)

    while uniqe_confirm:
        random_num = randint(2023000000000000, 2023999999999999)
        if not Card.objects.filter(number_card=random_num_card):
            break
    print('card_num = ', random_num_card)

def GetRandomAccount():
    random_num_account = randint(20230000000000000000, 20239999999999999999)

    uniqe_confirm = Card.objects.filter(number_card=random_num_account)

    while uniqe_confirm:
        random_num = randint(20230000000000000000, 20239999999999999999)
        if not Card.objects.filter(number_card=random_num_account):
            break
    print('account_num = ', random_num_account)


GetRandomCard()
GetRandomAccount()

def auth_view(request):
    username = request.POST["username"]  # допустим передали username и password
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        random_key = uuid.uuid4()
        session_storage.set(random_key, username)

        response = HttpResponse("{'status': 'ok'}")
        response.set_cookie("session_id", random_key)  # пусть ключем для куки будет session_id
        return response
    else:
        return HttpResponse("{'status': 'error', 'error': 'login failed'}")