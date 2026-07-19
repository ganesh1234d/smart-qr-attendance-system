const API_URL = window.location.origin + "/student/mark-attendance";

const token = localStorage.getItem("access_token");

// If user is not logged in
if (!token) {
    alert("Please login first.");
    window.location.href = "/login";
}

// Get session token from scanned QR URL (?session=xxxx)
const urlParams = new URLSearchParams(window.location.search);
const qrSession = urlParams.get("session");

// Swipe button
const swipeBtn = document.getElementById("swipeBtn");

swipeBtn.addEventListener("click", () => {

    if (!navigator.geolocation) {
        alert("GPS is not supported on this device.");
        return;
    }

    if (!qrSession) {
        alert("Invalid QR Code. Please scan today's attendance QR.");
        return;
    }

    swipeBtn.disabled = true;
    swipeBtn.innerHTML = "Getting Location...";

    navigator.geolocation.getCurrentPosition(

        async function(position) {

            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            try {

                const response = await fetch(API_URL, {

                    method: "POST",

                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + token
                    },

                    body: JSON.stringify({

                        latitude: latitude,
                        longitude: longitude,
                        qr_token: qrSession

                    })

                });

                const data = await response.json();

                if (response.ok) {

                    alert(data.message);

                    document.getElementById("attendanceStatus").innerHTML =
                        "Status : Present ✅";

                }
                else {

                    alert(data.detail);

                }

            }
            catch (err) {

                alert("Server Connection Failed");

            }

            swipeBtn.disabled = false;
            swipeBtn.innerHTML = "Swipe To Mark Attendance →";

        },

        function(error) {

            alert("Unable to get GPS location.");

            swipeBtn.disabled = false;
            swipeBtn.innerHTML = "Swipe To Mark Attendance →";

        }

    );

});