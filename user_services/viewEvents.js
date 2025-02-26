document.addEventListener("DOMContentLoaded", function () {
    const eventsTableBody = document.querySelector("#eventsTable tbody");

    // Dummy event data (replace this with API response later)
    const dummyEvents = [
        { id: 1, name: "Tech Conference 2025", date: "2025-03-10", location: "New York" },
        { id: 2, name: "AI Workshop", date: "2025-04-15", location: "San Francisco" },
        { id: 3, name: "Game Dev Meetup", date: "2025-05-20", location: "Los Angeles" }
    ];

    dummyEvents.forEach(event => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${event.name}</td>
            <td>${event.date}</td>
            <td>${event.location}</td>
            <td><button onclick="bookEvent('${event.id}')">Book</button></td>
        `;

        eventsTableBody.appendChild(row);
    });
});

// Example function to handle booking (for testing)
function bookEvent(eventId) {
    alert("Booking event ID: " + eventId);
}
