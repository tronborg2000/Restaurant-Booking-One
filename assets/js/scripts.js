document.addEventListener("DOMContentLoaded", function() {
    const bookingForm = document.getElementById("booking-form");
  
    if (bookingForm) {
      bookingForm.addEventListener("submit", function(event) {
        event.preventDefault();
        alert("Thank you for your booking! We will get back to you shortly.");
        bookingForm.reset();
      });
    }
  });
  