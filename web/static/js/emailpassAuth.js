async function loginWithEmail() {
    try {
        // Get email and password
        const email = document.getElementById("username_email").value.trim();
        const password = document.getElementById("password").value;

        // Basic validation
        if (!email || !password) {
            alert("Please enter your email and password.");
            return;
        }

        // Sign in using Firebase Email Authentication
        const result = await auth.signInWithEmailAndPassword(
            email,
            password
        );

        // Get Firebase ID token
        const token = await result.user.getIdToken();

        // Send token to Flask backend
        const response = await fetch("/verify-token", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                token: token
            })
        });

        const data = await response.json();

        // Check reposne
        if (!response.ok) {
            throw new Error(data.error || "Server error");
        }

        // Redirect to dashboard
        if (data.status === "success") {
            window.location.href = "/dashboard";
        } else {
            alert("Login failed: " + (data.error || "Unknown error"));
        }

    }
    catch (error) {
        console.error("Firebase Email Login Error:", error);
        alert("Firebase email login failed: " + error.message);
    }
}

// Attach event listener
document.addEventListener("DOMContentLoaded", () => {
    document
    .getElementById("emailLoginBtn")
    .addEventListener("click", loginWithEmail);
});