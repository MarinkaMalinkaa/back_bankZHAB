from django.contrib import admin
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import TokenProxy
from .models import Contract, Status, Account, Card, AuthUser, Transaction

# Register your models here.

# Описание администратора, добавляем ему таблицы, к которым есть доступ
admin.site.register(Contract)
admin.site.register(Status)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Card)
admin.site.register(AuthUser)

admin.site.unregister(TokenProxy)
admin.site.unregister(User)
admin.site.unregister(Group)



