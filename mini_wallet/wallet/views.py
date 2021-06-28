import json
from datetime import datetime
from base64 import b32encode

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.status import HTTP_400_BAD_REQUEST

from .constants import STATUS
from .serializer import AccountSerializer, WalletSerializer, WalletTransxSerializer, OTPSerializer
from .utils import IsAPIAuthenticated, GenerateOTP
from .api_exceptions import response_formatter


# Create your views here.
def index(request):
    return HttpResponse("Hello, This is virtual payment wallet.")


class Wallet(APIView):
    """
    View Class for enable & disable wallet and get wallet balance.
    """

    permission_classes = (IsAPIAuthenticated,)

    def post(self, request):
        requested_data = request.data
        account_id = requested_data.get('account_id')

        def _create_wallet():
            wallet_obj, created = WalletSerializer.create_wallet(account_id=account_id)

            if wallet_obj.is_deleted:
                _enable_wallet_if_not(wallet_obj.id)
                wallet_obj.is_deleted = False
            return wallet_obj

        def _enable_wallet_if_not(wallet_id):
            WalletSerializer.enable_wallet(wallet_id)

        wallet = _create_wallet()
        return self._prepare_response(account_id, wallet)

    def get(self, request):
        def _get_wallet():
            wallet_obj = WalletSerializer.get_wallet_by_account_id(account_id=requested_data.get('account_id'))
            if not wallet_obj:
                return response_formatter(HTTP_400_BAD_REQUEST, "Wallet Does Not Accept. First Enable it.")
            return wallet_obj

        requested_data = request.data
        wallet = _get_wallet()
        return self._prepare_response(requested_data['account_id'], wallet)

    def patch(self, request):
        requested_data = request.data
        wallet = WalletSerializer.get_wallet_by_account_id(account_id=requested_data['account_id'])
        WalletSerializer.disable_wallet(wallet_id=wallet.id)
        wallet.is_deleted = True
        return self._prepare_response(requested_data['account_id'], wallet)

    def _prepare_response(self, account_id, wallet):
        return Response(dict(
            status='success',
            data=dict(wallet=dict(
                id=wallet.id,
                owned_by=account_id,
                status=STATUS[wallet.is_deleted],
                enabled_at=wallet.created_at,
                balance=wallet.wallet_balance
            ))
        ))


class DepositMoney(APIView):
    """
    View Class for Deposit Money in the virtual wallet.
    """

    permission_classes = (IsAPIAuthenticated,)

    def post(self, request):
        def _deposit_balance():
            wallet_transx_obj = WalletTransxSerializer.add_transx(**request.data)
            wallet_balance = WalletSerializer.update_wallet_balance(request.data.get('wallet_id'))
            wallet_obj = WalletSerializer.get_wallet_by_wallet_id(wallet_id=request.data.get('wallet_id'))
            return wallet_obj, wallet_transx_obj

        def _prepare_response():
            return Response(dict(
                status="success",
                data=dict(
                    deposit=dict(
                        id=wallet_trnasx.id,
                        deposied_by=wallet.account_id,
                        status="success",
                        deposited_at=datetime.now(),
                        amount=wallet.wallet_balance,
                        reference_id=request.data.get('reference_id')
                    )
                )
            ))

        request.data['transx_type'] = 1
        account_id = request.data.pop('account_id')
        wallet, wallet_trnasx = _deposit_balance()
        return _prepare_response()


class WithdrawalMoney(APIView):
    """
    View Class for Withdraw Money from the virtual wallet.
    """

    permission_classes = (IsAPIAuthenticated,)

    def post(self, request):
        def _withdrawal_money():
            wallet_transx_obj = WalletTransxSerializer.add_transx(**request.data)
            wallet_balance = WalletSerializer.update_wallet_balance(request.data.get('wallet_id'))
            wallet_obj = WalletSerializer.get_wallet_by_wallet_id(wallet_id=request.data.get('wallet_id'))
            return wallet_obj, wallet_transx_obj

        def _prepare_response():
            return Response(dict(
                status="success",
                data=dict(
                    withdrawal=dict(
                        id=wallet_trnasx.id,
                        deposied_by=wallet.account_id,
                        status="success",
                        deposited_at=datetime.now(),
                        amount=wallet.wallet_balance,
                        reference_id=request.data.get('reference_id')
                    )
                )
            ))

        account_id = request.data.pop('account_id')
        wallet, wallet_trnasx = _withdrawal_money()
        return _prepare_response()


@authentication_classes([])
@permission_classes([AllowAny, ])
class Account(APIView):
    """
    A View Class for Creating Account & getting Account Information.
    """

    def post(self, request):
        if 'customer_xid' in request.data and request.data['customer_xid']:
            account = AccountSerializer.get_account(account_id=request.data['customer_xid'])
            account_id = account.id
        else:
            mobile_number = request.data['mobile_number']
            is_exists = AccountSerializer.is_account_exists(mobile_number)
            if is_exists:
                return Response(dict(
                    status="success",
                    data=dict(
                        message=f"Account already exists with mobile number {mobile_number}"
                    )
                ))
            account_id = AccountSerializer.create_account(
                name=request.data['name'],
                mobile_number=request.data['mobile_number']
            )
        token = b32encode(json.dumps(dict(account_id=str(account_id))).encode('utf-8'))
        return Response(dict(
            data=dict(
                token=token
            ),
            status='success'
        ))


class SendOTP(APIView):
    """
    A Class to generate OTP and send to customer's mobile number.
    """
    permission_classes = (IsAPIAuthenticated,)

    def post(self, request):
        account_id = request.data.pop('account_id')
        account = AccountSerializer.get_account(account_id=account_id)
        otp = GenerateOTP.generate()
        otp_id = OTPSerializer.generate_otp(otp, account)
        print(f"OTP is generated for account {account_id}, otp_id {otp_id}")

        return Response(dict(
            data=dict(
                message="OTP is sent to your registered account."
            ),
            status='success'
        ))


class VerifyAccount(APIView):
    """
    A class to verify account using OTP sent to mobile number.
    """

    permission_classes = (IsAPIAuthenticated,)

    def post(self, request):
        account_id = request.data.pop('account_id')
        account = AccountSerializer.get_account(account_id=account_id)
        otp = request.data.pop('otp')
        otp_obj = OTPSerializer.get_otp(account=account)

        if otp_obj.otp == otp:
            OTPSerializer.otp_verified(account)
            AccountSerializer.account_verified(account.id)

        return Response(dict(
            data=dict(
                message="Mobile Number is verified successfully."
            ),
            status='success'
        ))
