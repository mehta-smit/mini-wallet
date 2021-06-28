from rest_framework import serializers

from wallet.models import OtpVerification
from datetime import datetime


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpVerification
        fields = ('id', 'otp', 'is_verified', 'expired_at', 'created_at', 'modified_at', 'is_deleted')

    @classmethod
    def generate_otp(cls, otp, account):
        otp_obj = OtpVerification.objects.create(
            otp=otp,
            account=account
        )
        otp_obj.save()
        return otp_obj.id

    @classmethod
    def get_otp(cls, account):
        return OtpVerification.objects.filter(
            account=account,
            expired_at__lte=datetime.now()
        ).order_by('created_at').first()

    @classmethod
    def otp_verified(cls, account):
        return OtpVerification.objects.filter(
            account=account,
            expired_at__lte=datetime.now()
        ).update(is_verified=True)
