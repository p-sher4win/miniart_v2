// Google provider
const provider = new firebase.auth.GoogleAuthProvider();
provider.setCustomParameters({
    prompt: "select_account"
});

async function loginWithGoogle() {
    try {
        await firebase.auth().signOut();
        const result = await firebase.auth().signInWithPopup(provider);

        // Get Firebase ID token
        const token = await result.user.getIdToken();

        // Send token to Flask backend
        const response = await fetch("/verify-token", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ token: token })
        });

        if (!response.ok) {
            throw new Error("Server error");
        }

        const data = await response.json();

        if (data.status === "success") {
            // Redirect based on role
            // if (data.role === "admin") {
            //     window.location.href = "/admin";
            // } else {
            //     window.location.href = "/dashboard";
            // }
            console.log("Logged in as:", data.role);

            // Show on screen (better than console)
            const resultDiv = document.getElementById("result");

            if (data.role === "admin") {
                resultDiv.innerText = "✅ Logged in as ADMIN";
            } else {
                resultDiv.innerText = "✅ Logged in as OPERATOR";
            }
        }
        else {
            alert("Login failed: " + (data.error || "Unknown error"));
        }

    }
    catch (error) {
        console.error("Error:", error);
        alert("Google login failed: " + error.message);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    document
        .getElementById("googleLoginBtn")
        .addEventListener("click", loginWithGoogle);
});