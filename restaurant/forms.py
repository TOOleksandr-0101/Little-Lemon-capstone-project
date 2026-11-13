from django import forms

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["first_name", "reservation_date", "reservation_slot"]
        labels = {
            "first_name": "Name",
            "reservation_date": "Reservation date",
            "reservation_slot": "Reservation time",
        }
        widgets = {
            "first_name": forms.TextInput(
                attrs={"placeholder": "Your name", "autocomplete": "name"}
            ),
            "reservation_date": forms.DateInput(attrs={"type": "date"}),
            "reservation_slot": forms.Select(),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("reservation_date")
        slot = cleaned_data.get("reservation_slot")

        if date and slot:
            duplicate = Booking.objects.filter(
                reservation_date=date, reservation_slot=slot
            )
            if self.instance.pk:
                duplicate = duplicate.exclude(pk=self.instance.pk)
            if duplicate.exists():
                raise forms.ValidationError(
                    "This time is already booked. Please choose another time."
                )
        return cleaned_data
