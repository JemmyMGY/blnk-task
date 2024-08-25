from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.hashers import BCryptSHA256PasswordHasher
# Create your models here.
class Customer(models.Model):
    full_name = models.CharField(max_length=50, )
    email = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=32, validators=[MinLengthValidator(8)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.email
    # Automatically hash the password before saving
    def save(self):
        self.password = BCryptSHA256PasswordHasher.create(self.password)