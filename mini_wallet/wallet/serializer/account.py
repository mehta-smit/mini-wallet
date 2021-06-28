from rest_framework import serializers

from wallet.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'name', 'mobile_number', 'mobile_verified', 'created_at', 'modified_at', 'is_deleted')

    @classmethod
    def create_account(cls, name, mobile_number):
        account_obj = Account.objects.create(
            name=name,
            mobile_number=mobile_number
        )
        account_obj.save()
        return account_obj.id

    @classmethod
    def get_account(cls, account_id):
        return Account.objects.get(id=account_id)

    @classmethod
    def is_account_exists(cls, mobile_number):
        return Account.objects.filter(mobile_number=mobile_number).count()

    @classmethod
    def account_verified(cls, account_id):
        return Account.objects.filter(id=account_id).update(mobile_verified=True)
