from rest_framework import serializers

from wallet.constants import ACTIVE, DELETED
from wallet.models import Wallet

from .account import AccountSerializer


class WalletSerializer(serializers.ModelSerializer):
    account_id = AccountSerializer()

    class Meta:
        model = Wallet
        fields = ('id', 'account_id', 'wallet_balance', 'created_at', 'modified_at', 'is_deleted')

    @classmethod
    def get_wallet_by_wallet_id(cls, wallet_id):
        return Wallet.objects.get(id=wallet_id)

    @classmethod
    def get_wallet_by_account_id(cls, account_id):
        return Wallet.objects.get(account=account_id)

    @classmethod
    def enable_wallet(cls, wallet_id):
        return Wallet.objects.filter(id=wallet_id).update(is_deleted=ACTIVE)

    @classmethod
    def disable_wallet(cls, wallet_id):
        return Wallet.objects.filter(id=wallet_id).update(is_deleted=DELETED)

    @classmethod
    def create_wallet(cls, account_id):
        wallet = Wallet.objects.get_or_create(account_id=account_id)
        return wallet

    @classmethod
    def update_wallet_balance(cls, wallet_id):
        def _calculate_balance():
            from .wallet_transx import WalletTransxSerializer
            wallet_transx = WalletTransxSerializer.get_wallet_balance(wallet_id)
            wallet_balance = 0
            for transx in wallet_transx:
                if transx.transx_type:
                    wallet_balance += transx.amount
                else:
                    wallet_balance -= transx.amount
            return wallet_balance

        def _update_balance():
            return Wallet.objects.filter(id=wallet_id).update(wallet_balance=balance)

        balance = _calculate_balance()
        _update_balance()
        return balance
