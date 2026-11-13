from datetime import date

from django.contrib import messages
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET

from .forms import BookingForm
from .models import Booking


def home(request):
    return render(request, "restaurant/index.html")


def booking(request):
    initial = {"reservation_date": date.today().isoformat()}
    form = BookingForm(request.POST or None, initial=initial)

    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                form.save()
        except IntegrityError:
            form.add_error(
                None, "This time is already booked. Please choose another time."
            )
        else:
            messages.success(request, "Your table has been booked.")
            return redirect("booking")

    return render(request, "restaurant/booking.html", {"form": form})


@require_GET
def bookings_api(request):
    bookings = Booking.objects.all()
    requested_date = request.GET.get("date")

    if requested_date:
        try:
            date.fromisoformat(requested_date)
        except ValueError:
            return JsonResponse(
                {"error": "Date must use YYYY-MM-DD format."}, status=400
            )
        bookings = bookings.filter(reservation_date=requested_date)

    data = [
        {
            "id": item.id,
            "first_name": item.first_name,
            "reservation_date": item.reservation_date.isoformat(),
            "reservation_slot": item.reservation_slot,
            "time": item.get_reservation_slot_display(),
        }
        for item in bookings
    ]
    return JsonResponse({"bookings": data})
