from django.contrib import admin
from payment.models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_method', 'payment_amount', 'status', 'created_at', 'paid_at')
    search_fields = ('order__order_number', 'transaction_id')
    list_filter = ('payment_method', 'status', 'created_at')

admin.site.register(Payment, PaymentAdmin)
