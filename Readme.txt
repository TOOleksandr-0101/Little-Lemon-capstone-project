LITTLE LEMON API - PATHS FOR REVIEW

Base URL: http://127.0.0.1:8000

1. Public menu API
GET  /api/menu-items/
GET  /api/menu-items/{id}/

Menu changes require an admin token:
POST   /api/menu-items/
PUT    /api/menu-items/{id}/
PATCH  /api/menu-items/{id}/
DELETE /api/menu-items/{id}/

Example menu body:
{
  "title": "Greek salad",
  "price": "12.50",
  "featured": true
}

2. User registration and authentication
POST /api/register/
Body:
{
  "username": "reviewer",
  "email": "reviewer@example.com",
  "password": "review-pass-123"
}

POST /api/token/
Body:
{
  "username": "reviewer",
  "password": "review-pass-123"
}

Copy the returned token into this Insomnia header:
Authorization: Token YOUR_TOKEN_HERE

3. Booking API (token required)
GET    /api/bookings/
GET    /api/bookings/?date=2026-12-20
POST   /api/bookings/
GET    /api/bookings/{id}/
PUT    /api/bookings/{id}/
PATCH  /api/bookings/{id}/
DELETE /api/bookings/{id}/

Example booking body:
{
  "first_name": "Sofia",
  "reservation_date": "2026-12-20",
  "reservation_slot": 17
}

4. Original booking page and JSON endpoint
GET /booking/
GET /bookings
GET /bookings?date=2026-12-20

Run the project:
pipenv install
pipenv shell
python manage.py migrate
python manage.py runserver
