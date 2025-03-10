from django.contrib.auth.models import User
from PIL import Image
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    profile_pin = models.IntegerField(blank=False, null=False, default=2002)

    def __str__(self):
        return f'{self.user.username} profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)


        if img.height > 300  or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path, quality=95)


class Transfer(models.Model):
    DEBIT = 'Debit'
    CREDIT = 'Credit'
    TRANSACTION_TYPE_CHOICES = [
        (DEBIT, 'Debit'),
        (CREDIT, 'Credit'),
    ]
    PENDING = 'Pending'
    COMPLETED = 'Completed'
    TRANSACTION_TYPE_INFO = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
    ]
    INTERNATIONAL = 'International Transfer'
    LOCAL = 'Local Transfer'
    CHECK = 'Check Deposite'
    TRANSACTION_SCOPE = [
        (INTERNATIONAL, 'Local Transfer'),
        (LOCAL, 'Local Check'),
        (CHECK, 'Check Deposite'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    account_number = models.CharField(max_length=15)
    amount = models.IntegerField(blank=False, null=False)
    bank_name = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=250, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    transaction_pin = models.IntegerField(blank=False, null=False)
    transfer_date = models.DateField(default=timezone.now)
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES,
        default=DEBIT,
    )
    transaction_info = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_INFO,
        default=PENDING,
    )
    transaction_scope = models.CharField(
        max_length=50,
        choices=TRANSACTION_SCOPE,
        default=LOCAL,
    )

    def clean(self):
        if len(str(self.transaction_pin)) != 4:
            raise ValidationError("Transaction PIN must be exactly 4 digits.")

    def __str__(self):
        return f"{self.bank_name}, {self.account_number}, {self.amount}"
    

class Chatbox(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    message = models.CharField(max_length=1000)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    

class IMFVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='imf_verification')
    imf_code = models.CharField(max_length=10, unique=True, null=True, blank=True)  # Allow null
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"IMF Code for {self.user.email}"
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pin_code = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.user.email