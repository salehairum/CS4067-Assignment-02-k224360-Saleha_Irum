document.querySelector("form").addEventListener("submit", async function (event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        // Send POST request to FastAPI backend
        const response = await fetch("/api/user/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Unknown error");
        }

        const result = await response.json();
        console.log("User created:", result);

        window.location.href = `viewEvents.html?username=${result.username}&balance=${result.balance}&id=${result.id}`;
    } catch (error) {
        console.error("Error:", error.message);
        alert(error.message); // Display error to user
    }
}); 