document.addEventListener("DOMContentLoaded", async function () {
    const eventsTableBody = document.querySelector("#eventsTable tbody");

    try {
        // Call User API instead of Event Service directly
        const response = await fetch("http://127.0.0.1:8000/users/events/");
        if (!response.ok) throw new Error("Failed to fetch events");

        const events = await response.json();

        events.forEach(event => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${event.name}</td>
                <td>${event.date}</td>
                <td>${event.location}</td>
                <td>${event.ticket_price} Rs</td>
                <td><button onclick="bookEvent('${event.id}')">Book</button></td>
            `;

            eventsTableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Error fetching events:", error);
    }
});

document.querySelector(".viewBooking").addEventListener("click", function () {
    // Construct the URL with query parameters
    const url = `viewBookings.html?username=${encodeURIComponent(userData.username)}&balance=${encodeURIComponent(userData.balance)}`;

    // Redirect to the new page
    window.location.href = url;
});

function bookEvent(eventId) {
    console.log("Booking event with ID:", eventId);

    // Open the modal (if using a modal-based approach)
    const modal = document.getElementById("ticketModal");
    modal.style.display = "flex";
    const closeModal = document.querySelector(".close");
    closeModal.addEventListener("click", () => {
        modal.style.display = "none";
    });
}
