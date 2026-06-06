from flask import Flask, render_template, request, redirect, url_for

from db import (
    create_tables,
    insert_sample_data,
    get_all_enquiries,
    add_enquiry,
    delete_enquiry,
    get_dashboard_counts
)

app = Flask(
    __name__,
    template_folder="template",
    static_folder="static",
    static_url_path=""
)

create_tables()
insert_sample_data()


@app.route("/")
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