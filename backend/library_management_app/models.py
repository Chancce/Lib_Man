from django.db import models
import uuid
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

AVAILABLE = 'AVAILABLE'
NOT_AVAILABLE = 'NOT_AVAILABLE'
AVAILABILITY_STATUS_OPTIONS = [
    (AVAILABLE, 'Available'),
    (NOT_AVAILABLE, 'Not Available'),
]

ISSUED = 'ISSUED'
RETURNED = 'RETURNED'
STATUS_CHOICES = [
    (ISSUED, 'Issued'),
    (RETURNED, 'Returned'),
]

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    quantity = models.IntegerField(default=1)
    daily_fee = models.DecimalField(max_digits=6, decimal_places=2, default=30.00)
    availability_status = models.CharField(max_length=30, choices=AVAILABILITY_STATUS_OPTIONS, default=AVAILABLE)
    status_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def book_availability(self):
        if self.quantity > 0:
            return f"Available ({self.quantity})"
        else:
            return "Not Available"

@receiver(post_save, sender=Book)
@receiver(post_delete, sender=Book)
def update_book_availability(sender, instance, **kwargs):
    if instance.quantity > 0:
        instance.availability_status = AVAILABLE
    else:
        instance.availability_status = NOT_AVAILABLE
    instance.save()



class Member(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    outstanding_debt = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    def can_borrow(self):
        return self.outstanding_debt <= 500

class Transaction (models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    issue_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ISSUED)
    fee_charged = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    @property
    def total_fee(self):
        days_borrowed = (self.return_date - self.issue_date).days if self.return_date else 0
        return days_borrowed * self.book.daily_fee

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.issue_status == RETURNED:
            self.member.outstanding_debt += self.fee_charged
            self.member.save()