from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from django.contrib.auth.hashers import BCryptSHA256PasswordHasher
from django.utils import timezone


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=32, validators=[MinLengthValidator(8)])
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f'{self.id} => {self.full_name} - {self.email}'

    def save(self, *args, **kwargs):
        hasher = BCryptSHA256PasswordHasher()
        self.password = hasher.encode(self.password, salt=hasher.salt())
        super().save(*args, **kwargs)

class LoanRequest(models.Model):
    STATUS_OPTIONS = (
        ("PENDING", "PENDING"),
        ("APPROVED", "APPROVED"),
        ("REJECTED", "REJECTED"),
    )
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    duration = models.IntegerField(validators=[MaxValueValidator(120), MinValueValidator(12)])
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=8, choices=STATUS_OPTIONS, default="PENDING")