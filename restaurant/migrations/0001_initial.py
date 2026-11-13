from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Booking",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("reservation_date", models.DateField()),
                (
                    "reservation_slot",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (10, "10:00"),
                            (11, "11:00"),
                            (12, "12:00"),
                            (13, "13:00"),
                            (14, "14:00"),
                            (15, "15:00"),
                            (16, "16:00"),
                            (17, "17:00"),
                            (18, "18:00"),
                            (19, "19:00"),
                            (20, "20:00"),
                        ]
                    ),
                ),
            ],
            options={"ordering": ["reservation_date", "reservation_slot"]},
        ),
        migrations.AddConstraint(
            model_name="booking",
            constraint=models.UniqueConstraint(
                fields=("reservation_date", "reservation_slot"),
                name="unique_booking_date_and_slot",
            ),
        ),
    ]
