const token = localStorage.getItem("access_token");

if(!token){

    window.location.href = "/login";

}

const generateBtn = document.getElementById("generateBtn");

const qrDiv = document.getElementById("qrcode");

const sessionInfo = document.getElementById("sessionInfo");


generateBtn.addEventListener("click", async function(){

    generateBtn.disabled = true;

    generateBtn.innerHTML = "Generating...";

    try{

        const response = await fetch(

            window.location.origin + "/admin/generate-qr-session",

            {

                method: "POST",

                headers: {

                    "Authorization": "Bearer " + token

                }

            }

        );

        const data = await response.json();

        if(response.ok){

            // Build the URL students will scan
            const attendanceUrl =
                window.location.origin +
                "/student/attendance-page?session=" +
                data.session_id;

            // Clear old QR
            qrDiv.innerHTML = "";

            // Generate QR code using image API (no external JS library needed)
            const qrImageUrl =
                "https://api.qrserver.com/v1/create-qr-code/?size=260x260&data=" +
                encodeURIComponent(attendanceUrl);

            const qrImg = document.createElement("img");
            qrImg.src = qrImageUrl;
            qrImg.alt = "Attendance QR Code";

            qrDiv.appendChild(qrImg);

            sessionInfo.innerHTML =
                "Session ID: " + data.session_id +
                "<br>Valid for: " + data.valid_date;

        }
        else{

            alert(data.detail || "Failed to generate QR.");

        }

    }
    catch(error){

        console.log(error);

        alert("Server Connection Failed");

    }

    generateBtn.disabled = false;

    generateBtn.innerHTML = "🔄 Generate New QR for Today";

});