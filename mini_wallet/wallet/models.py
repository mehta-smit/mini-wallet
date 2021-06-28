from uuid import uuid4

from django.db import models
import datetime

# Create your models here.


class BaseClass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Account(BaseClass):
    id = models.UUIDField(primary_key=True, default=uuid4(), editable=False)
    name = models.CharField(null=False, max_length=20)
    mobile_number = models.CharField(null=False, max_length=10)
    mobile_verified = models.BooleanField(null=False, default=False)

    class Meta:
        default_related_name = 'account'

    objects = models.Manager()


class Wallet(BaseClass):
    id = models.UUIDField(primary_key=True, default=uuid4(), editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    wallet_balance = models.FloatField(default=0, null=False)

    class Meta:
        default_related_name = 'wallet'

    objects = models.Manager()


class WalletTransx(BaseClass):
    id = models.UUIDField(primary_key=True, default=uuid4(), editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    reference_id = models.UUIDField(default=uuid4(), null=False)
    amount = models.FloatField(null=False, default=0)
    transx_type = models.BooleanField(default=0, null=False)  # withdrawal = 0, deposit = 1
    status = models.BooleanField(default=1, null=False)  # success = 1, failure = 0

    class Meta:
        default_related_name = 'wallet_transaction'

    objects = models.Manager()


class OtpVerification(BaseClass):
    id = models.UUIDField(primary_key=True, default=uuid4(), editable=False)
    otp = models.BigIntegerField(blank=False, null=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    is_verified = models.BooleanField(null=False, default=False)
    expired_at = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(minutes=20))
