from django.db import models
from authentication.models import User
# Create your models here.

class Expenses(models.Model):

    CATEGORY_OPTIONS = {
        ('OPERATING EXPENSE', 'operating expense'),
        ('RENT', 'RENT'),
        ('TRAVEL', 'TRAVEL'),
        ('FOOD', 'FOOD'),
        ('OTHERS', 'OTHERS'),
    }

    category = models.CharField(choices=CATEGORY_OPTIONS, max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    description = models.TextField(null=False, blank=False)
    date = models.DateField(null=False, blank=False)