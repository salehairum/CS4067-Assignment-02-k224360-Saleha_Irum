function getUserId() {
    const params = new URLSearchParams(window.location.search);
    return {
        id: params.get("id")
    };
}

const container = document.getElementById('notifications');
function updateNoNotificationsMessage() {
    if (container.children.length === 0) {
        container.innerHTML = `<div class="notification no-notifications">No notifications</div>`;
    }
}

function addNotification(booking_id) {
    // Remove "No notifications" message if present
    const noNotifElement = document.querySelector('.no-notifications');
    if (noNotifElement) noNotifElement.remove();

    const notification = document.createElement('div');
    notification.classList.add('notification');
    notification.setAttribute("data-booking-id", booking_id);

    notification.innerHTML = `
        <span>Booking with booking id ${booking_id} has been made successfully.</span>
        <button class="close-btn" onclick="removeNotification(this)">&times;</button>
    `;

    container.appendChild(notification);

}

function removeNotification(element) {
    const notification = element.parentElement;
    const bookingId = notification.getAttribute("data-booking-id");

    if (!bookingId) {
        console.error("No booking ID found for this notification.");
        return;
    }

    // Make DELETE request to API
    fetch(`http://localhost:5001/notifications/delete/${bookingId}`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.message === "Notification deleted successfully") {
                notification.remove();
                updateNoNotificationsMessage();

                return fetch(`http://localhost:5000/bookings/${bookingId}/status`, { // Assuming booking API is on port 5002
                    method: "PATCH", // Or "PUT" if your API requires that
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ status: "confirmed" }) // Update status to "confirmed"
                });
            } else {
                console.error("Failed to delete notification:", data.error);
            }
        })
        .catch(error => console.error("Error deleting notification:", error));
}

document.addEventListener("DOMContentLoaded", async function () {

    try {
        const id = parseInt(getUserId().id, 10);
        const response = await fetch(`http://127.0.0.1:5001/notifications/${id}`);
        if (!response.ok) throw new Error("Failed to fetch notifications");

        const notifs = await response.json();

        notifs.forEach(notif => {
            addNotification(notif.booking_id);
        });
        updateNoNotificationsMessage();
    } catch (error) {
        console.error("Error fetching notifications:", error);
    }
});

document.querySelector(".viewEvent").addEventListener("click", function () { openNewPage("viewEvents"); });
document.querySelector(".viewBooking").addEventListener("click", function () { openNewPage("viewBookings"); });

function openNewPage(pageName) {
    const id = parseInt(getUserId().id, 10);
    const balance = document.getElementById("balance").textContent.split(": ")[1];
    // Construct the URL with query parameters
    const url = `${pageName}.html?username=${encodeURIComponent(userData.username)}&balance=${encodeURIComponent(balance)}&id=${encodeURIComponent(id)}`;

    // Redirect to the new page
    window.location.href = url;
}
