from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from customers.models import Customer, LoanRequest


class Provider(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    total_fund= models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.id} || {self.name} - {self.email} - {self.total_fund}'


class Loan(models.Model):
    STATUS_OPTIONS = (
        ("PENDING", "PENDING"),
        ("APPROVED", "APPROVED"),
        ("REJECTED", "REJECTED"),
    )
    id = models.AutoField(primary_key=True)
    loan_request = models.OneToOneField(LoanRequest, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=9, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=9, decimal_places=2, default=total_amount)
    paid_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    interest_rate = models.DecimalField(max_digits=2, decimal_places=2, default=.20)
    duration = models.IntegerField(validators=[MaxValueValidator(120),MinValueValidator(12)])
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=8, choices=STATUS_OPTIONS, default="PENDING")

    def __str__(self) -> str:
        return f'{self.id}'


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    paid_amount = models.DecimalField(max_digits=9, decimal_places=2)
    paid_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f'{self.id}'
