from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps

from db import (
    create_tables,
    insert_sample_data,
    get_all_enquiries,
    add_enquiry,
    delete_enquiry,
    get_dashboard_counts,
    create_user,
    get_user_by_email,
    check_user_password,
)

app = Flask(
    __name__,
    template_folder="template",
    static_folder="static",
    static_url_path=""
)

app.secret_key = "barca"

create_tables()
insert_sample_data()

def login_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return route_function(*args, **kwargs)
    return wrapper

@app.route("/")
def default_page():
    if "user_id" in session:
        return redirect(url_for("home"))
    return redirect(url_for("login"))


@app.route("/signup.html", methods=["GET", "POST"])
def signup():
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if name == "" or email == "" or password == "" or confirm_password == "":
            error = "Please fill all fields."
        elif len(password) < 6:
            error = "Password must be at least 6 characters."
        elif password != confirm_password:
            error = "Passwords do not match."
        elif get_user_by_email(email):
            error = "This email is already registered. Please login."
        else:
            create_user(name, email, password)
            return redirect(url_for("login"))

    return render_template("signup.html", error=error)

@app.route("/login.html", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = get_user_by_email(email)

        if user and check_user_password(user, password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["mail"]=user["email"]
            return redirect(url_for("home"))

        error = "Invalid email or password."

    return render_template("login.html", error=error)

@app.route("/logout.html")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/index.html")
def home():
    return render_template("index.html")

@app.route("/aboutus.html")
def about():
    return render_template("aboutus.html")

@app.route("/services.html")
def services():
    return render_template("services.html")

@app.route("/dashboard.html")
def dashboard():
    counts = get_dashboard_counts()
    enquiries = get_all_enquiries()

    return render_template(
        "dashboard.html",
        counts=counts,
        enquiries=enquiries
    )


@app.route("/contact.html", methods=["GET","POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        service = request.form.get("service")
        message = request.form.get("message")

        add_enquiry(name, email, phone, service, message)

        return redirect(url_for("thank_you"))
    
    return render_template("contact.html")


@app.route("/thankyou.html")
def thank_you():
    return render_template("thankyou.html")


@app.route("/admin.html")
def admin():
    enquiries = get_all_enquiries()
    return render_template("admin.html", enquiries=enquiries)

@app.route("/delete/<int:enquiry_id>")
def delete(enquiry_id):
    delete_enquiry(enquiry_id)
    return redirect(url_for("admin"))


@app.route("/student.html")
def student_profile():
    return render_template("student.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)