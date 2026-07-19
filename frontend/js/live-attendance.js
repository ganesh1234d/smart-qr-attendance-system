const token = localStorage.getItem("access_token");

fetch(window.location.origin + "/admin/live-attendance",{
    headers:{

        "Authorization":"Bearer "+token

    }

})

.then(res=>res.json())

.then(data=>{

    let rows="";

    data.forEach(student=>{

        rows+=`

        <tr>

            <td>${student.student_id}</td>

            <td>${student.name}</td>

            <td>${student.batch_no}</td>

            <td>${student.department}</td>

            <td>${student.time}</td>

            <td>${student.status}</td>

            <td>${student.latitude}</td>

            <td>${student.longitude}</td>

        </tr>

        `;

    });

    document.getElementById("attendanceTable").innerHTML=rows;

})

.catch(error=>{

    console.log(error);

    alert("Unable to load attendance.");

});