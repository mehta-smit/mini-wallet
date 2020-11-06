from django.contrib import admin
from django.apps import apps


from wallet.models import Account, Wallet, WalletTransx


# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'modified_at', 'is_deleted')
    search_fields = ('id', )


class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'account_id', 'wallet_balance', 'created_at', 'modified_at', 'is_deleted')
    search_fields = ('id', 'account_id', 'wallet_balance')


class WalletTransAdmin(admin.ModelAdmin):
    list_display = ('id', 'wallet_id', 'reference_id', 'amount', 'transx_type', 'status', 'created_at', 'modified_at', 'is_deleted', )
    search_fields = ('id', 'wallet_id', 'reference_id', 'amount', 'transx_type', 'status', 'is_deleted')


admin.site.register(Account, AccountAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(WalletTransx, WalletTransAdmin)


admin.site.site_header = "Mini Wallet"
