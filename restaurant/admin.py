from django.contrib import admin

from .models import Booking, MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "featured")
    list_filter = ("featured",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("first_name", "reservation_date", "reservation_slot")
    list_filter = ("reservation_date",)
    ordering = ("reservation_date", "reservation_slot")
