from rest_framework import serializers

from wallet.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'created_at', 'modified_at', 'is_deleted')

    @classmethod
    def create_account(cls):
        account_obj = Account.objects.create()
        account_obj.save()
        return account_obj.id

    @classmethod
    def get_account(cls, account_id):
        return Account.objects.get(id=account_id)
