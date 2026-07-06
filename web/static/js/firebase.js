// Firebase Config
const firebaseConfig = window.FIREBASE_CONFIG;

// Initialize Firebase
if (!firebase.apps.length) {
    firebase.initializeApp(firebaseConfig);
}

const auth = firebase.auth();