function submitEnquiry(event){
    const name=document.getElementById("name").value.trim();
    const email=document.getElementById("email").value.trim();
    const service=document.getElementById("service").value.trim();
    const message=document.getElementById("message").value.trim();
    const formMessage=document.getElementById("formMessage");

    if(name===""||email===""||service===""||message===""){
        formMessage.textContent="Please fill all fields before submitting!!";
        formMessage.style.color="red";
        return;
    }
    formMessage.textContent = "Thank you, " + name + "! Your enquiry has been recorded for the demo.";
    formMessage.style.color = "#123c69";
}