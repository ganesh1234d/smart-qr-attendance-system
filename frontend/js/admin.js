const API_URL = window.location.origin + "/student";

const token = localStorage.getItem("access_token");

if(!token){

    window.location.href="/login";

}

async function loadDashboard(){

    const headers={

        "Authorization":"Bearer "+token

    };

    // Total Students
    let response = await fetch(
        API_URL+"/admin/total-students",
        {headers}
    );

    let data = await response.json();

    document.getElementById("totalStudents").innerHTML =
        data.total_students;


    // Today's Attendance
    response = await fetch(
        API_URL+"/admin/today-attendance",
        {headers}
    );

    data = await response.json();

    document.getElementById("todayAttendance").innerHTML =
        data.present;


    // Absent Students
    response = await fetch(
        API_URL+"/admin/absent-count",
        {headers}
    );

    data = await response.json();

    document.getElementById("absentStudents").innerHTML =
        data.absent;

}

loadDashboard();


function viewStudents(){
    window.location.href = "/admin/students-page";
}

function liveAttendance(){
    window.location.href = "/admin/live-attendance-page";
}

function reports(){
    window.location.href = "/admin/reports-page";
}

function logout(){

    localStorage.removeItem("access_token");

    window.location.replace("/");

}