document.addEventListener("DOMContentLoaded", async function () {
    const bookingsTableBody = document.querySelector("#bookingsTable tbody");

    try {
        // Call User API instead of Event Service directly
        const userId = 1;   //chaaaaaaaaaaaaange
        const response = await fetch(`http://127.0.0.1:5000/bookings/user/${userId}`);
        if (!response.ok) throw new Error("Failed to fetch bookings");

        const bookings = await response.json();

        bookings.forEach(booking => {
            const row = document.createElement("tr");

            const createdAt = new Date(booking.created_at).toLocaleString();
            row.innerHTML = `
                <td>${booking.event_id}</td>
                <td>${booking.status}</td>
                <td>${createdAt}</td>
            `;
            // <td><button onclick="confirmBooking('${booking.id}')">Confirm</button></td>

            bookingsTableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Error fetching bookings:", error);
    }
});


document.querySelector(".viewEvent").addEventListener("click", function () {
    // Construct the URL with query parameters
    const url = `viewEvents.html?username=${encodeURIComponent(userData.username)}&balance=${encodeURIComponent(userData.balance)}`;

    // Redirect to the new page
    window.location.href = url;
});

