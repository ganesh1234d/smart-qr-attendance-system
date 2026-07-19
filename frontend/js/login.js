const API_URL = window.location.origin + "/student/login";

const form = document.getElementById("loginForm");

form.addEventListener("submit", async function(e){

    e.preventDefault();

    const email = document.getElementById("email").value;

    const password = document.getElementById("password").value;

    try{

        const response = await fetch(API_URL,{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                email:email,

                password:password

            })

        });

        const data = await response.json();

        if(response.ok){

            localStorage.setItem(
                "access_token",
                data.access_token
            );

            document.getElementById("message").style.color="green";

            document.getElementById("message").innerHTML="Login Successful";

            setTimeout(function(){

                // Redirect based on role
                if(data.role === "Admin"){

                    window.location.href = "/admin/dashboard-page";

                }
                else{

                    window.location.href = "/student/attendance-page";

                }

            },1000);

        }
        else{

            document.getElementById("message").style.color="red";

            document.getElementById("message").innerHTML=data.detail;

        }

    }

    catch(error){

        console.log(error);

        document.getElementById("message").style.color="red";

        document.getElementById("message").innerHTML="Server Connection Failed";

    }

});