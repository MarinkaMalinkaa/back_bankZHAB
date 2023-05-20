from random import randint

from rest_framework import viewsets
from bank.serializers import UserSerializer, UserFilter, AccountSerializer, CardSerializer, ContractSerializer, TransactionSerializer, StatusSerializer, AccountFilter, ContractFilter
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
import smtplib
import time
from email.mime.text import MIMEText
from datetime import datetime


def my_view(request):
    # Получаем данные из запроса
    id_card = request.GET.get('id_card')
    number_card = request.GET.get('number_card')
    cvc = request.GET.get('cvc')
    contract_id = request.GET.get('contract_id')

    user_online = is_user_online(request)
    print(user_online)
    if user_online:
        pin = 0
    else:
        pin = 1
    # Создаем объект запроса и заполняем данными
    my_request = MyRequest(
        id_card=int(id_card),
        number_card=int(number_card),
        cvc=int(cvc),
        pin=int(pin),
        contract_id=int(contract_id)
    )

    # Создаем объект клиента и отправляем запрос
    try:
        channel = grpc.insecure_channel('localhost:50051')
        my_stub = MyServiceStub(channel)
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
    except grpc.RpcError as e:
        # Обрабатываем ошибку
        if e.code() == grpc.StatusCode.UNAVAILABLE:
            return HttpResponse('Сервер недоступен', status=500)
        else:
            return HttpResponse(str(e), status=500)

def admin_online(request):
    request.session['last_activity'] = datetime.now().timestamp()
    return HttpResponse('Обновлено')

def is_user_online(request):
    last_activity_str = request.session.get('last_activity')
    if last_activity_str:
        last_activity = datetime.fromtimestamp(float(last_activity_str))
        time_since_last_activity = (datetime.now() - last_activity).total_seconds()
        if time_since_last_activity <= 300:
            return True
    return False



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
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AccountFilter
    search_fields = ['^authuser']


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
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ContractFilter
    search_fields = ['^status', '^auth_user']


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
        random_num_account = randint(20230000000000000000, 20239999999999999999)
        if not Account.objects.filter(account_num=random_num_account):
            break
    return HttpResponse(format(random_num_account))


def GetRandomCVC(request):
    random_cvc = randint(111, 999)
    return HttpResponse('cvc = {}'.format(random_cvc))


def GetRandomPin(request):
    random_pin = randint(1111, 9999)
    return HttpResponse('pin = {}'.format(random_pin))


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
