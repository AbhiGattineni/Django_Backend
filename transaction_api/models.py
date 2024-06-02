import shortuuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_subsidiary(value):
    valid_subsidiaries = ['AMS', 'ACS', 'ASS', 'APS', 'ATI']
    if value not in valid_subsidiaries:
        raise ValidationError(f"{value} is not a valid subsidiary")

def validate_transaction_type(value):
    valid_transaction_types = ['credit', 'debit']
    if value not in valid_transaction_types:
        raise ValidationError(f"{value} is not a valid transaction type")
    
def validate_payment_type(value):
    valid_transaction_types = ['cash', 'upi', 'bank_transfer']
    if value not in valid_transaction_types:
        raise ValidationError(f"{value} is not a valid payment type")

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]
    
    PAYMENT_TYPE_CHOICES = [
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    SUBSIDIARY_CHOICES = [
        ('AMS', 'AMS'),
        ('ACS', 'ACS'),
        ('ASS', 'ASS'),
        ('APS', 'APS'),
        ('ATI', 'ATI'),
    ]

    transaction_id = models.CharField(max_length=22, default=shortuuid.uuid, editable=False, unique=True)
    receiver_name = models.CharField(max_length=100, blank=False, null=False)
    receiver_id = models.CharField(max_length=50, blank=False, null=False)
    sender_name = models.CharField(max_length=100, blank=False, null=False)
    sender_id = models.CharField(max_length=50, blank=False, null=False)
    accountant_name = models.CharField(max_length=100, blank=False, null=False)
    accountant_id = models.CharField(max_length=50, blank=False, null=False)
    credited_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    debited_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    transaction_datetime = models.DateTimeField(blank=False, null=False)
    uploaded_datetime = models.DateTimeField(default=timezone.now, blank=False, null=False)
    transaction_type  = models.CharField(max_length=50, blank=False, null=False, choices=TRANSACTION_TYPE_CHOICES, validators=[validate_transaction_type])
    payment_type = models.CharField(max_length=50, blank=False, null=False, choices=PAYMENT_TYPE_CHOICES, validators=[validate_payment_type])
    subsidiary = models.CharField(max_length=20, blank=False, null=False, choices=SUBSIDIARY_CHOICES, validators=[validate_subsidiary])
    currency = models.CharField(max_length=3, blank=False, null=False)
    description = models.TextField(blank=False, null=False)

    class Meta:
        db_table = 'transactions'

    def __str__(self):
        return f"{self.sender_name} to {self.receiver_name} on {self.transaction_datetime}"
