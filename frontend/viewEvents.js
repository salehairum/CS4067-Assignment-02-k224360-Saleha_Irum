function getUserId() {
    const params = new URLSearchParams(window.location.search);
    return {
        id: params.get("id")
    };
}

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

document.querySelector(".viewBooking").addEventListener("click", function () { openNewPage("viewBookings"); });
document.querySelector(".notification-btn").addEventListener("click", function () { openNewPage("notifications"); });

function openNewPage(pageName) {
    const id = parseInt(getUserId().id, 10);
    // Construct the URL with query parameters
    const url = `${pageName}.html?username=${encodeURIComponent(userData.username)}&balance=${encodeURIComponent(userData.balance)}&id=${encodeURIComponent(id)}`;

    // Redirect to the new page
    window.location.href = url;
}

function bookEvent(eventId) {
    console.log("Booking event with ID:", eventId);

    // Open the modal (if using a modal-based approach)
    const modal = document.getElementById("ticketModal");
    modal.style.display = "flex";
    const closeModal = document.querySelector(".close");
    closeModal.addEventListener("click", () => {
        modal.style.display = "none";
    });
    document.getElementById("confirmBooking").onclick = function () {
        confirmBooking(eventId);
    };
}

async function getTicketPrice(eventId) {
    try {
        console.log(eventId);
        const response = await fetch(`http://127.0.0.1:8080/api/events/${eventId}/price`);
        if (!response.ok) throw new Error("Failed to get ticket price");

        const price = await response.json();
        return price;
    } catch (error) {
        console.error("Error fetching ticket price:", error.message);
        return null;
    }
}

async function confirmBooking(eventId) {
    const ticketCount = document.getElementById("ticketCount").value;

    if (ticketCount < 1) {
        alert("Please select at least one ticket.");
        return;
    }

    try {
        const ticketPrice = await getTicketPrice(eventId);
        if (ticketPrice === null) {
            alert("Failed to retrieve ticket price. Please try again.");
            return;
        }

        const totalCost = ticketPrice * ticketCount;
        const id = parseInt(getUserId().id, 10);
        const response = await fetch("http://127.0.0.1:8000/users/bookings/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                event_id: eventId,
                user_id: id,
                price: totalCost,
                ticket_count: ticketCount
            })
        });

        const result = await response.json();
        if (!response.ok) throw new Error(`Booking failed-> ${result.detail}`);

        alert("Booking confirmed!");
        document.getElementById("ticketModal").style.display = "none";

        document.getElementById("balance").textContent = "Balance: " + result.remaining_balance;
    } catch (error) {
        alert("Error: " + error.message);
    }
}