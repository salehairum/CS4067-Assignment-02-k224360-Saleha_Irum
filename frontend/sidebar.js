function getQueryParams() {
    const params = new URLSearchParams(window.location.search);
    return {
        username: params.get("username"),
        balance: params.get("balance"),
        id: params.get("id")
    };
}

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

const userData = getQueryParams();
document.getElementById("username").textContent = "Username: " + userData.username;
document.getElementById("balance").textContent = "Balance: " + userData.balance;
const userId = parseInt(userData.id, 10);
fetchNotificationCount(userId);
