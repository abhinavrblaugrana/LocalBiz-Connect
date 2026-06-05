function showMessage() {
    document.getElementById("message").textContent =
        "Great! Day 2 continues from Day 1 with more pages and better design.";
}

function submitEnquiry(event) {
    event.preventDefault();
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const service = document.getElementById("service").value.trim();
    const message = document.getElementById("message").value.trim();
    const formMessage = document.getElementById("formMessage");
    if (name === "" || email === "" || service === "" || message === "") {
        formMessage.textContent = "Please fill all fields before submitting.";
        formMessage.style.color = "red";
        return;
    }
    formMessage.textContent = "Thank you, " + name + "! Your enquiry has been recorded for the Day 2 demo.";
    formMessage.style.color = "#123c69";
}
