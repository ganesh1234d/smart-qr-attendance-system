const token = localStorage.getItem("access_token");

if(token==null){

    window.location.href="/login";

}

fetch(window.location.origin + "/student/profile",{

headers:{

Authorization:"Bearer "+token

}

})

.then(response=>response.json())

.then(data=>{

document.getElementById("studentName").innerHTML="Welcome, "+data.name;

})

.catch(error=>{

console.log(error);

});

document.getElementById("logoutBtn").addEventListener("click",function(){

localStorage.removeItem("access_token");

window.location.href="/login";

});

document.getElementById("scanBtn").addEventListener("click",function(){

alert("QR Scanner will be added in next step.");

});