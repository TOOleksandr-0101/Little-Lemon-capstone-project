from django.db import models


class MenuItem(models.Model):
    title = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Booking(models.Model):
    SLOT_CHOICES = [(hour, f"{hour}:00") for hour in range(10, 21)]

    first_name = models.CharField(max_length=100)
    reservation_date = models.DateField()
    reservation_slot = models.PositiveSmallIntegerField(choices=SLOT_CHOICES)

    class Meta:
        ordering = ["reservation_date", "reservation_slot"]
        constraints = [
            models.UniqueConstraint(
                fields=["reservation_date", "reservation_slot"],
                name="unique_booking_date_and_slot",
            )
        ]

    def __str__(self):
        return f"{self.first_name} - {self.reservation_date} at {self.reservation_slot}:00"
