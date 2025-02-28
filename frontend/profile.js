function getQueryParams() {
    const params = new URLSearchParams(window.location.search);
    return {
        username: params.get("username"),
        balance: params.get("balance")
    };
}

const userData = getQueryParams();
console.log(userData);
document.getElementById("username").textContent = "Username: " + userData.username;
document.getElementById("balance").textContent = "Balance: " + userData.balance;
