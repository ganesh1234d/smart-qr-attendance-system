const API_URL = window.location.origin + "/student/register";

const form = document.getElementById("registerForm");

form.addEventListener("submit", async function (e) {

    e.preventDefault();

    const message = document.getElementById("message");

    message.innerHTML = "";
    message.style.color = "red";

    const full_name = document.getElementById("full_name").value.trim();

    const email = document.getElementById("email").value.trim();

    const batch_no = document.getElementById("batch_no").value.trim();

    const password = document.getElementById("password").value;

    // ==========================================
    // NAME VALIDATION
    // Only letters and spaces allowed
    // ==========================================

    if (!/^[A-Za-z ]+$/.test(full_name)) {

        message.innerHTML = "Numbers and special characters are not allowed in Name.";

        return;

    }

    // ==========================================
    // BATCH NO VALIDATION
    // Only numbers (1 to 5 digits)
    // ==========================================

    if (!/^\d{1,5}$/.test(batch_no)) {

        message.innerHTML = "Batch No must contain only 1 to 5 digits.";

        return;

    }

    const data = {

        full_name: full_name,

        email: email,

        batch_no: batch_no,

        password: password

    };

    try {

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify(data)

        });

        const result = await response.json();

        if (response.ok) {

            message.style.color = "green";

            message.innerHTML = result.message;

            form.reset();

            setTimeout(() => {

                window.location.href = "/login";

            }, 2000);

        }

        else {

            message.style.color = "red";

            if (Array.isArray(result.detail)) {

                message.innerHTML = result.detail.map(err => err.msg).join("<br>");

            } else {

                message.innerHTML = result.detail || "Registration Failed";

            }

        }

    }

    catch (error) {

        message.style.color = "red";

        message.innerHTML = "Cannot connect to server.";

        console.log(error);

    }

});