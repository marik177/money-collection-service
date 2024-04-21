import sys
from datetime import datetime, timedelta

from django.db import models

from collection_project.users.models import BaseModel, BaseUser


class Occasion(BaseModel):
    """Occasion model"""

    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Collection(BaseModel):
    """Group money collections"""

    author = models.ForeignKey(BaseUser, related_name="author", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    occasion = models.ForeignKey(Occasion, related_name="collection", on_delete=models.PROTECT)
    description = models.TextField()
    planned_amount = models.PositiveIntegerField(default=sys.maxsize)
    cover_image = models.ImageField(upload_to="collection_covers/")
    end_collection_date = models.DateTimeField(default=datetime.utcnow() + timedelta(days=7))

    def __str__(self) -> str:
        return self.title


class Payment(BaseModel):
    """Individual payment"""

    collection = models.ForeignKey(Collection, related_name="payments", on_delete=models.CASCADE)
    contributor = models.ForeignKey(BaseUser, related_name="payment", on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Payment {self.amount}"
