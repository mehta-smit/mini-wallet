import binascii
import json
from base64 import b32encode, b32decode

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .api_exceptions import AuthenticationFailed
from .serializer import AccountSerializer, WalletSerializer


class CustomAuthentication(TokenAuthentication):
    def __init__(self):
        pass

    def _create_auth_token(self, claims):
        claims_dump = json.dumps(claims)
        token = b32encode(claims_dump.encode('utf-8'))
        return token

    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token or len(token.split()) != 2:
            raise AuthenticationFailed('Invalid token header. No credentials provided.')

        token = token.split()[-1]
        try:
            claim = json.loads(b32decode(token).decode('utf-8'))
        except (TypeError, UnicodeDecodeError, binascii.Error):
            raise AuthenticationFailed('Invalid basic header. Credentials not correctly base64 encoded.')

        account = AccountSerializer.get_account(account_id=claim['account_id'])

        if not account or account.is_deleted:
            raise AuthenticationFailed('Invalid Account or Account inactive or deleted.')
        request.data['account_id'] = account.id

        wallet = WalletSerializer.get_wallet_by_account_id(account_id=account.id)
        if wallet or not wallet.is_deleted:
            request.data['wallet_id'] = wallet.id
        setattr(request, 'account', account)
        return account, wallet


class IsAPIAuthenticated(IsAuthenticated):
    def __init__(self):
        pass

    def has_permission(self, request, view):
        return request.account and not request.account.is_deleted
