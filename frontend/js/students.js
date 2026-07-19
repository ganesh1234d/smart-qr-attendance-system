const token = localStorage.getItem("access_token");

fetch(window.location.origin + "/admin/students",{

    headers:{

        "Authorization":"Bearer "+token

    }

})

.then(res=>res.json())

.then(data=>{

    let table="";

    data.forEach(student=>{

        table+=`

        <tr>

            <td>${student.student_id}</td>

            <td>${student.full_name}</td>

            <td>${student.batch_no}</td>

            <td>${student.email}</td>


        </tr>

        `;

    });

    document.getElementById("studentTable").innerHTML=table;

});