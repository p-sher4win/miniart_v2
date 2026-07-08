// Google provider
const provider = new firebase.auth.GoogleAuthProvider();

provider.setCustomParameters({
    prompt: "select_account"
});

async function loginWithGoogle() {
    try {
        // Sign-in Google popup
        const result = await auth.signInWithPopup(provider);

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
        }
        else {
            alert("Login failed: " + (data.error || "Unknown error"));
        }

    }
    catch (error) {
        console.error("Google Login Error:", error);
        alert("Google login failed: " + error.message);
    }
}

// Google login button
document.addEventListener("DOMContentLoaded", () => {
    document
        .getElementById("googleLoginBtn")
        .addEventListener("click", loginWithGoogle);
});
