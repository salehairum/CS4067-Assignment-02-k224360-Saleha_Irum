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
        const response = await fetch("/api/user/users/events/");
        if (!response.ok) throw new Error("Failed to fetch events");

        const events = await response.json();

        document.querySelector(".loadingMsg").style.display = "none";

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



function updateNotificationCount(count) {
    const notifBadge = document.querySelector('.notification-count');
    if (count > 0) {
        notifBadge.textContent = count;
        notifBadge.style.display = "flex";
    } else {
        notifBadge.style.display = "none";
    }
}

async function fetchNotificationCount(userId) {
    try {
        const response = await fetch(`/api/notification/notifications/${userId}/count`);
        if (!response.ok) {
            throw new Error("Failed to fetch notification count");
        }

        const data = await response.json();
        updateNotificationCount(data.notification_count);
    } catch (error) {
        console.error("Error fetching notification count:", error);
    }
}

document.querySelector(".viewBooking").addEventListener("click", function () { openNewPage("viewBookings"); });
document.querySelector(".notification-btn").addEventListener("click", function () { openNewPage("notifications"); });

const userId = parseInt(getUserId().id, 10);
fetchNotificationCount(userId);
function openNewPage(pageName) {
    const id = parseInt(getUserId().id, 10);
    const balance = document.getElementById("balance").textContent.split(": ")[1];
    // Construct the URL with query parameters
    const url = `${pageName}.html?username=${encodeURIComponent(userData.username)}&balance=${encodeURIComponent(balance)}&id=${encodeURIComponent(id)}`;

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
        const response = await fetch(`/api/event/api/events/${eventId}/price`);
        if (!response.ok) throw new Error("Failed to get ticket price");

        const price = await response.json();
        return price;
    } catch (error) {
        console.error("Error fetching ticket price:", error.message);
        return null;
    }
}

async function confirmBooking(eventId) {
    document.getElementById("processBooking").style.display = "block";

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
        const response = await fetch("/api/user/users/bookings/", {
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

        fetchNotificationCount(id);
    } catch (error) {
        alert("Error: " + error.message);
    }
}