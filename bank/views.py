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
from django.shortcuts import render
from bank.grpc_client import MyStub
from django.http import HttpResponse
from django.http import JsonResponse
from bank.my_proto_pb2 import MyRequest
from bank.my_proto_pb2_grpc import MyServiceStub
import grpc


def my_view(request):
    id_card = request.GET.get('id_card')
    number_card = request.GET.get('number_card')
    cvc = request.GET.get('cvc')
    pin = request.GET.get('pin')
    contract_id = request.GET.get('contract_id')
    # Создаем объект запроса и заполняем данными
    my_request = MyRequest(
        id_card=int(id_card),
        number_card=int(number_card),
        cvc=int(cvc),
        pin=int(pin),
        contract_id=int(contract_id)
    )

    # Создаем объект клиента
    channel = grpc.insecure_channel('localhost:50051')
    my_stub = MyServiceStub(channel)

    # Отправляем запрос и получаем ответ
    response = my_stub.MyMethod(my_request)

    # Обрабатываем ответ
    my_response = {
        'id_card': response.id_card,
        'number_card': response.number_card,
        'cvc': response.cvc,
        'pin': response.pin,
        'contract_id': response.contract_id,
    }

    # Возвращаем ответ в виде JSON
    return JsonResponse(my_response)
   # return render(request, './my_template.html', context)


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


def GetRandomCard(request):
    random_num_card = randint(2023000000000000, 2023999999999999)

    uniqe_confirm = Card.objects.filter(number_card=random_num_card)

    while uniqe_confirm:
        random_num_card = randint(2023000000000000, 2023999999999999)
        if not Card.objects.filter(number_card=random_num_card):
            break
    return HttpResponse("card_num = {}".format(random_num_card))


def GetRandomAccount(request):
    random_num_account = randint(20230000000000000000, 20239999999999999999)

    uniqe_confirm = Account.objects.filter(account_num=random_num_account)

    while uniqe_confirm:
        random_num = randint(20230000000000000000, 20239999999999999999)
        if not Account.objects.filter(account_num=random_num_account):
            break
    return HttpResponse('account_num = {}'.format(random_num_account))


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
