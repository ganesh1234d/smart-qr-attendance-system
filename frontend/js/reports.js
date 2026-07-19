const token = localStorage.getItem("access_token");
let attendanceChart = null;
function loadReport() {

    const selectedDate =
        document.getElementById("reportDate").value;

    let url =
    window.location.origin + "/admin/report";

    if (selectedDate !== "") {

        url += "?report_date=" + selectedDate;

    }

    fetch(url, {

        method: "GET",

        headers: {

            "Authorization": "Bearer " + token

        }

    })

    .then(response => response.json())

    .then(data => {

        document.getElementById("totalStudents").innerHTML =
            data.total_students;

        document.getElementById("presentStudents").innerHTML =
            data.present;

        document.getElementById("absentStudents").innerHTML =
            data.absent;

        document.getElementById("attendancePercentage").innerHTML =
            data.attendance_percentage + "%";





        // ================================
// Attendance Pie Chart
// ================================

const ctx = document.getElementById("attendanceChart");

if (attendanceChart !== null) {

    attendanceChart.destroy();

}

attendanceChart = new Chart(ctx, {

    type: "pie",

    data: {

        labels: [

            "🟢 Present",

            "🔴 Absent"

        ],

        datasets: [

            {

                data: [

                    data.present,

                    data.absent

                ],

                backgroundColor: [

                    "#5dba60",

                    "#e56a61"

                ],

                borderColor: "#ffffff",

                borderWidth: 1,

                hoverOffset: 8

            }

        ]

    },

    options: {

        responsive: true,

        plugins: {

            legend: {

                position: "bottom"

            }

        }

    }

});

        let rows = "";

        data.students.forEach(student => {
            let badge = "";

if (student.status === "Present") {

    badge = `
        <span class="present-badge">
            🟢 Present
        </span>
    `;

}
else {

    badge = `
        <span class="absent-badge">
            🔴 Absent
        </span>
    `;

}

rows += `

<tr>

    <td>${student.student_id}</td>

    <td>${student.name}</td>

    <td>${student.batch_no}</td>

    <td>${student.department}</td>

    <td>${student.time}</td>

    <td>${badge}</td>

</tr>

`;



        });

        document.getElementById("reportTable").innerHTML =
            rows;

    })

    .catch(error => {

        console.log(error);

        alert("Unable to load report.");

    });

}

// Load today's report automatically
loadReport();


// =====================================
// SEARCH STUDENT
// =====================================

function searchStudent() {

    let input = document
        .getElementById("searchInput")
        .value
        .toLowerCase();

    let table = document.getElementById("reportTable");

    let rows = table.getElementsByTagName("tr");

    for (let i = 0; i < rows.length; i++) {

        let name = rows[i].cells[1].innerText.toLowerCase();

        let roll = rows[i].cells[2].innerText.toLowerCase();

        if (
            name.includes(input) ||
            roll.includes(input)
        ) {

            rows[i].style.display = "";

        }
        else {

            rows[i].style.display = "none";

        }

    }

}



function exportExcel() {

    const token = localStorage.getItem("access_token");

    const selectedDate =
        document.getElementById("reportDate").value;

    let url =
    "http://127.0.0.1:8000/admin/export-excel";

    if (selectedDate !== "") {

        url += "?report_date=" + selectedDate;

    }

    fetch(url, {

        method: "GET",

        headers: {

            "Authorization": "Bearer " + token

        }

    })

    .then(response => {

        if (!response.ok) {

            throw new Error("Export failed");

        }

        return response.blob();

    })

    .then(blob => {

        const link = document.createElement("a");

        link.href = window.URL.createObjectURL(blob);

        link.download = "Attendance_Report.xlsx";

        link.click();

    })

    .catch(error => {

        console.log(error);

        alert("Unable to export Excel.");

    });

}