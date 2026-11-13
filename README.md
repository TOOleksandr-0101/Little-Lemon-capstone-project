# Little Lemon booking project

Final Django project for the Little Lemon booking assignment.

The default database engine is MySQL. The `restaurant` app is registered in
`INSTALLED_APPS`, and the initial migration is included in the project.

## Setup

1. Install MySQL and create the database:

   ```sql
   CREATE DATABASE littlelemon CHARACTER SET utf8mb4;
   ```

2. In this folder, install the environment and dependencies:

   ```bash
   pip install pipenv
   pipenv install
   pipenv shell
   ```

3. Copy `.env.example` to `.env`, then set your local MySQL username and password.
   Export the variables from that file in your terminal before running Django. For example:

   ```bash
   export MYSQL_DATABASE=littlelemon
   export MYSQL_USER=root
   export MYSQL_PASSWORD=your_mysql_password
   export MYSQL_HOST=127.0.0.1
   export MYSQL_PORT=3306
   ```

4. Apply the included migration and start the server:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

Open `http://127.0.0.1:8000/booking/`.

## API

- Menu: `http://127.0.0.1:8000/api/menu-items/`
- Registration: `http://127.0.0.1:8000/api/register/`
- Token: `http://127.0.0.1:8000/api/token/`
- REST bookings: `http://127.0.0.1:8000/api/bookings/`
- Original JSON bookings: `http://127.0.0.1:8000/bookings`
- Original JSON bookings by date: `http://127.0.0.1:8000/bookings?date=2026-12-13`

See `Readme.txt` for ready-to-copy Insomnia requests and example JSON bodies.

The database prevents two bookings from using the same date and time. The form also disables reserved time slots when the selected date changes.

The booking page contains the three required fields: name, reservation date and
reservation time. It uses the browser date picker, selects today's date when the
page opens, refreshes bookings with `fetch()` after a date change, and displays
`No Booking` when the selected day is empty.

## Test without a local MySQL server

SQLite is available only as a convenient test fallback:

```bash
DATABASE_ENGINE=sqlite python manage.py test
```

The normal/default project configuration uses MySQL.
