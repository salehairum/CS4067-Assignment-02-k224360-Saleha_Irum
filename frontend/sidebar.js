function getQueryParams() {
    const params = new URLSearchParams(window.location.search);
    return {
        username: params.get("username"),
        balance: params.get("balance"),
        id: params.get("id")
    };
}


const userData = getQueryParams();
document.getElementById("username").textContent = "Username: " + userData.username;
document.getElementById("balance").textContent = "Balance: " + userData.balance;