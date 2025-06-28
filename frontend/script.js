window.onload = function () {
    const savedEmail = localStorage.getItem("savedEmail");
    const savedTheme = localStorage.getItem("theme");
    if (savedEmail) document.getElementById("loginEmail").value = savedEmail;
    if (savedTheme === "dark") document.body.classList.add("dark");
    if (localStorage.getItem("isLoggedIn")) showMainContent();
};

function showLogin() {
    document.getElementById("loginForm").classList.add("active-form");
    document.getElementById("signupForm").classList.remove("active-form");
    document.getElementById("loginBtn").classList.add("active");
    document.getElementById("signupBtn").classList.remove("active");
}

function showSignup() {
    document.getElementById("signupForm").classList.add("active-form");
    document.getElementById("loginForm").classList.remove("active-form");
    document.getElementById("signupBtn").classList.add("active");
    document.getElementById("loginBtn").classList.remove("active");
}

function togglePassword(id) {
    const field = document.getElementById(id);
    field.type = field.type === "password" ? "text" : "password";
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function disableButton(formId) {
    const form = document.getElementById(formId);
    const btn = form.querySelector("button[type='submit']");
    btn.disabled = true;
    setTimeout(() => btn.disabled = false, 2000);
}

function validateLogin(event) {
    event.preventDefault();
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;
    if (!isValidEmail(email)) {
        alert("Please enter a valid email.");
        return false;
    }
    fetch("http://localhost:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            if (document.getElementById("rememberMe").checked) {
                localStorage.setItem("savedEmail", email);
            } else {
                localStorage.removeItem("savedEmail");
            }
            localStorage.setItem("isLoggedIn", "true");
            alert("Login successful!");
            showMainContent();
        } else {
            alert(data.message || "Login failed!");
        }
    });
    disableButton("loginForm");
    return false;
}

function validateSignup(event) {
    event.preventDefault();
    const email = document.getElementById("signupEmail").value;
    const pass = document.getElementById("signupPassword").value;
    const confirm = document.getElementById("confirmPassword").value;
    if (!isValidEmail(email)) {
        alert("Please enter a valid email.");
        return false;
    }
    if (pass.length < 6) {
        alert("Password must be at least 6 characters.");
        return false;
    }
    if (pass !== confirm) {
        alert("Passwords do not match.");
        return false;
    }
    if (!document.getElementById("privacyPolicy").checked || !document.getElementById("terms").checked) {
        alert("Please agree to the Privacy Policy and Terms.");
        return false;
    }
    fetch("http://localhost:5000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password: pass })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            localStorage.setItem("isLoggedIn", "true");
            alert("Signup successful!");
            showMainContent();
        } else {
            alert(data.message || "Signup failed!");
        }
    });
    disableButton("signupForm");
    return false;
}

function toggleTheme() {
    document.body.classList.toggle("dark");
    localStorage.setItem("theme", document.body.classList.contains("dark") ? "dark" : "light");
}

function showMainContent() {
    document.getElementById("authSection").style.display = "none";
    document.getElementById("mainContent").style.display = "block";
    showSection("home");
}

function showSection(sectionId) {
    document.querySelectorAll(".content-section").forEach(section => {
        section.style.display = "none";
    });
    document.getElementById(sectionId).style.display = "block";
}

function logout() {
    localStorage.removeItem("isLoggedIn");
    document.getElementById("authSection").style.display = "block";
    document.getElementById("mainContent").style.display = "none";
    document.getElementById("loginEmail").value = localStorage.getItem("savedEmail") || "";
    showLogin();
}

// === ONLY UPDATED FUNCTIONS BELOW ===

function predictAllocation() {
    const text = document.getElementById("allocationInput").value;
    const avgReturn = parseFloat(document.getElementById("avgReturn").value);
    const cluster = parseInt(document.getElementById("cluster").value);
    if (!text || isNaN(avgReturn) || isNaN(cluster)) {
        document.getElementById("allocationResult").innerHTML = "<p class='text-danger'>Please fill all fields.</p>";
        return;
    }
    fetch("http://localhost:5000/allocation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, avg_return: avgReturn, cluster })
    })
    .then(res => res.json())
    .then(data => {
        let html = `<p>Sentiment Score: ${data.sentiment_score || 0}</p><h4>Recommended Allocation</h4><ul>`;
        html += `<li>Cash: ${Math.round(data.allocation[0] * 100)}%</li>`;
        html += `<li>BTC: ${Math.round(data.allocation[1] * 100)}%</li>`;
        html += `<li>ETH: ${Math.round(data.allocation[2] * 100)}%</li>`;
        html += "</ul>";
        document.getElementById("allocationResult").innerHTML = html;
    })
    .catch(error => {
        document.getElementById("allocationResult").innerHTML = "<p class='text-danger'>Error fetching allocation.</p>";
    });
}

function runBacktest() {
    const startDate = document.getElementById("startDate").value;
    const endDate = document.getElementById("endDate").value;
    if (!startDate || !endDate) {
        document.getElementById("backtestResult").innerHTML = "<p class='text-danger'>Please select dates.</p>";
        return;
    }
    fetch("http://localhost:5000/backtest", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ start_date: startDate, end_date: endDate })
    })
    .then(res => res.json())
    .then(data => {
        let html = `<h4>Portfolio Value Over Time</h4><p>Final Value: $${data.final_value}</p>`;
        html += "<h4>Asset Allocations</h4><ul>";
        data.allocations.forEach((alloc, i) => {
            html += `<li>Step ${i + 1}: Cash ${Math.round(alloc[0] * 100)}%, BTC ${Math.round(alloc[1] * 100)}%, ETH ${Math.round(alloc[2] * 100)}%</li>`;
        });
        html += "</ul>";
        document.getElementById("backtestResult").innerHTML = html;
    })
    .catch(error => {
        document.getElementById("backtestResult").innerHTML = "<p class='text-danger'>Error running backtest.</p>";
    });
}
