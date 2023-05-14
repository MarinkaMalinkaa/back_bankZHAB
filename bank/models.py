from django.db import models

# Create your models here.

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    phone = models.CharField(max_length=11, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_user'


class Account(models.Model):
    authuser = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    account_num = models.CharField(max_length=20)
    balance = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'account'


class Card(models.Model):
    number_card = models.CharField(max_length=16, blank=True, null=True)
    cvc = models.IntegerField(blank=True, null=True)
    pin = models.IntegerField(blank=True, null=True)
    contract = models.ForeignKey('Contract', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'card'


class Status(models.Model):
    flag = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'status'


class Contract(models.Model):
    status = models.ForeignKey(Status, models.DO_NOTHING, blank=True, null=True)
    account = models.ForeignKey(Account, models.DO_NOTHING, blank=True, null=True)
    auth_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'contract'


class Transaction(models.Model):
    sum_transaction = models.IntegerField(blank=True, null=True)
    account1 = models.ForeignKey(Account, models.DO_NOTHING, blank=True, null=True)
    account2 = models.ForeignKey(Account, models.DO_NOTHING, related_name='transaction_account2_set', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'transaction'
