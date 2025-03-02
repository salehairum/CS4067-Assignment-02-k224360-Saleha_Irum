function getUserId() {
    const params = new URLSearchParams(window.location.search);
    return {
        id: params.get("id")
    };
}

document.addEventListener("DOMContentLoaded", async function () {
    const bookingsTableBody = document.querySelector("#bookingsTable tbody");

    try {
        // Call User API instead of Event Service directly

        const id = parseInt(getUserId().id, 10);
        const response = await fetch(`http://127.0.0.1:5000/bookings/user/${id}`);
        if (!response.ok) throw new Error("Failed to fetch bookings");

        const bookings = await response.json();

        bookings.forEach(booking => {
            const row = document.createElement("tr");

            const createdAt = new Date(booking.created_at).toLocaleString();
            row.innerHTML = `
                <td>${booking.event_id}</td>
                <td>${booking.status}</td>
                <td>${createdAt}</td>
                <td><button onclick="confirmBooking('${booking.id}')">Confirm</button></td>
            `;

            bookingsTableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Error fetching bookings:", error);
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
        const response = await fetch(`http://127.0.0.1:5001/notifications/${userId}/count`);
        if (!response.ok) {
            throw new Error("Failed to fetch notification count");
        }

        const data = await response.json();
        updateNotificationCount(data.notification_count);
    } catch (error) {
        console.error("Error fetching notification count:", error);
    }
}

document.querySelector(".viewEvent").addEventListener("click", function () { openNewPage("viewEvents"); });
document.querySelector(".notification-btn").addEventListener("click", function () { openNewPage("notifications"); });

const userId = parseInt(userData.id, 10);
fetchNotificationCount(userId);
function openNewPage(pageName) {
    const id = parseInt(getUserId().id, 10);
    const balance = document.getElementById("balance").textContent.split(": ")[1];
    // Construct the URL with query parameters
    const url = `${pageName}.html?username=${encodeURIComponent(userData.username)}&balance=${encodeURIComponent(balance)}&id=${encodeURIComponent(id)}`;

    // Redirect to the new page
    window.location.href = url;
}
