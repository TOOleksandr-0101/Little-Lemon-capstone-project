const dateInput = document.querySelector("#id_reservation_date");
const slotSelect = document.querySelector("#id_reservation_slot");
const bookingsList = document.querySelector("#bookings-list");
const bookingCount = document.querySelector("#booking-count");

function localDateString() {
  const now = new Date();
  const offset = now.getTimezoneOffset() * 60000;
  return new Date(now.getTime() - offset).toISOString().slice(0, 10);
}

function setSlotAvailability(bookings) {
  const reservedSlots = new Set(bookings.map((booking) => String(booking.reservation_slot)));

  Array.from(slotSelect.options).forEach((option) => {
    if (!option.value) return;
    const isReserved = reservedSlots.has(option.value);
    option.disabled = isReserved;
    option.textContent = `${option.value}:00${isReserved ? " — booked" : ""}`;
  });

  if (slotSelect.selectedOptions[0]?.disabled) {
    slotSelect.value = "";
  }
}

function showBookings(bookings) {
  bookingCount.textContent = bookings.length;

  if (bookings.length === 0) {
    bookingsList.innerHTML = '<p class="empty">No Booking</p>';
    return;
  }

  bookingsList.innerHTML = bookings
    .map(
      (booking) => `
        <div class="booking-row">
          <span class="booking-time">${booking.time}</span>
          <span>${booking.first_name}</span>
        </div>`
    )
    .join("");
}

async function loadBookings() {
  if (!dateInput.value) return;

  bookingsList.innerHTML = '<p class="loading">Loading…</p>';

  try {
    const response = await fetch(`/bookings?date=${encodeURIComponent(dateInput.value)}`);
    if (!response.ok) throw new Error("Could not load bookings");

    const data = await response.json();
    showBookings(data.bookings);
    setSlotAvailability(data.bookings);
  } catch (error) {
    bookingCount.textContent = "—";
    bookingsList.innerHTML = '<p class="empty error-text">Could not load bookings.</p>';
  }
}

if (!dateInput.value) {
  dateInput.value = localDateString();
}
dateInput.min = localDateString();

dateInput.addEventListener("change", loadBookings);
loadBookings();
