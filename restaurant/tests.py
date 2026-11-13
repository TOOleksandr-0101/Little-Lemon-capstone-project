from datetime import date

from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Booking, MenuItem


class BookingTests(TestCase):
    def setUp(self):
        self.booking = Booking.objects.create(
            first_name="Mario",
            reservation_date=date(2026, 12, 13),
            reservation_slot=18,
        )

    def test_booking_page_has_three_fields(self):
        response = self.client.get(reverse("booking"))
        self.assertContains(response, 'name="first_name"')
        self.assertContains(response, 'name="reservation_date"')
        self.assertContains(response, 'name="reservation_slot"')
        self.assertContains(response, 'type="date"')

    def test_api_returns_all_bookings(self):
        response = self.client.get(reverse("bookings_api"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["bookings"]), 1)

    def test_api_filters_by_date(self):
        response = self.client.get(reverse("bookings_api"), {"date": "2026-12-13"})
        self.assertEqual(response.json()["bookings"][0]["first_name"], "Mario")

        empty = self.client.get(reverse("bookings_api"), {"date": "2026-12-14"})
        self.assertEqual(empty.json()["bookings"], [])

    def test_duplicate_date_and_slot_is_rejected_by_form(self):
        response = self.client.post(
            reverse("booking"),
            {
                "first_name": "Luigi",
                "reservation_date": "2026-12-13",
                "reservation_slot": 18,
            },
        )
        self.assertContains(response, "This time is already booked")
        self.assertEqual(Booking.objects.count(), 1)

    def test_database_constraint_rejects_duplicates(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Booking.objects.create(
                    first_name="Luigi",
                    reservation_date=date(2026, 12, 13),
                    reservation_slot=18,
                )


class RestApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="tester", password="strong-pass-123"
        )
        self.token = Token.objects.create(user=self.user)
        MenuItem.objects.create(title="Greek salad", price="12.50", featured=True)

    def test_menu_is_public(self):
        response = self.client.get("/api/menu-items/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["title"], "Greek salad")

    def test_user_can_register_and_receives_token(self):
        response = self.client.post(
            "/api/register/",
            {
                "username": "newuser",
                "email": "new@example.com",
                "password": "new-password-123",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("token", response.data)

    def test_user_can_obtain_token(self):
        response = self.client.post(
            "/api/token/",
            {"username": "tester", "password": "strong-pass-123"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["token"], self.token.key)

    def test_authenticated_user_can_create_booking(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.post(
            "/api/bookings/",
            {
                "first_name": "Sofia",
                "reservation_date": "2026-12-20",
                "reservation_slot": 17,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["time"], "17:00")

    def test_booking_api_requires_authentication(self):
        response = self.client.get("/api/bookings/")
        self.assertEqual(response.status_code, 401)
