document.querySelector("form").addEventListener("submit", async function (event) {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const balance = document.getElementById("balance").value;

    const userData = {
        email: email,
        username: username,
        password: password,
        balance: parseFloat(balance)  // Ensure balance is a number
    };

    try {
        // Send POST request to FastAPI backend
        const response = await fetch("http://user_service:8000/users/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(userData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail); // Show error from backend
        }

        const result = await response.json();
        console.log("User created:", result);
        window.location.href = `viewEvents.html?username=${result.username}&balance=${result.balance}&id=${result.id}`;
    } catch (error) {
        console.error("Error:", error.message);
        alert(error.message); // Display error to user
    }
}); 