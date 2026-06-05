from flask import Flask, render_template

app = Flask(
    __name__,
    template_folder="frontend",
    static_folder="frontend",
    static_url_path=""
)


@app.route("/")
@app.route("/index.html")
def home():
    return render_template("index.html")

@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/services.html")
def services():
    return render_template("services.html")

@app.route("/dashboard.html")
def dashboard():
    return render_template("dashboard.html")

@app.route("/contact.html")
def contact():
    return render_template("contact.html")

@app.route("/student_profile.html")
def student_profile():
    return render_template("student_profile.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)