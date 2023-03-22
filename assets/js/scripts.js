function sendEmail(templateParams) {
  emailjs.send("YOUR_SERVICE_ID", "YOUR_TEMPLATE_ID", templateParams)
    .then(
      function (response) {
        console.log("SUCCESS!", response.status, response.text);
      },
      function (error) {
        console.log("FAILED...", error);
      }
    );
}

document.addEventListener("DOMContentLoaded", function () {
  const bookingForm = document.getElementById("booking-form");

  if (bookingForm) {
    bookingForm.addEventListener("submit", function (event) {
      event.preventDefault();

      // Send booking email
      const bookingDetails = {
        name: event.target.name.value,
        email: event.target.email.value,
        phone: event.target.phone.value,
        date: event.target.date.value,
        time: event.target.time.value,
        guests: event.target.guests.value,
        tables: event.target.tables.value,
      };

      sendEmail(bookingDetails);

      alert("Thank you for your booking! We will get back to you shortly.");
      bookingForm.reset();
    });
  }

  const cancelBookingForm = document.getElementById("cancel-booking-form");

  if (cancelBookingForm) {
    cancelBookingForm.addEventListener("submit", function (event) {
      event.preventDefault();

      // Send cancellation email
      const bookingId = event.target.booking_id.value;
      const cancelDetails = {
        booking_id: bookingId,
      };

      sendEmail(cancelDetails);

      alert("Your booking has been canceled. We will get back to you shortly.");
      cancelBookingForm.reset();
    });
  }
});
