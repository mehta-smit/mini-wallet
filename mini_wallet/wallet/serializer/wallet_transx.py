from rest_framework import serializers

from wallet.models import WalletTransx
from .wallet import WalletSerializer


class WalletTransxSerializer(serializers.ModelSerializer):
    wallet_id = WalletSerializer()

    class Meta:
        model = WalletTransx
        fields = (
        'id', 'wallet_id', 'reference_id', 'amount', 'transx_type', 'status', 'created_at', 'modified_at', 'is_deleted')

    @classmethod
    def get_wallet_balance(cls, wallet_id):
        wallet_transx = WalletTransx.objects.all().filter(wallet_id=wallet_id)
        return wallet_transx

    @classmethod
    def add_transx(cls, wallet_id, reference_id, amount, transx_type=0):
        return WalletTransx.objects.create(
            wallet_id=wallet_id,
            reference_id=reference_id,
            amount=amount,
            transx_type=transx_type
        )
