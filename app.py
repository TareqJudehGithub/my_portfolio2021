from flask import Flask, render_template, request
from datetime import datetime
import csv, os, smtplib

year = datetime.now().year
app = Flask(__name__)
my_user = os.environ.get("EMAIL_USER")
my_password = os.environ.get("EMAIL_PASS")


@app.route('/')
def hello_world():
    """Main page"""
    return render_template("index.html", year=year)


@app.route("/<string:page_name>")
def html_page(page_name):
    """Accessing portfolio HTML pages"""
    return render_template(page_name, year=year)


@app.route("/submit_form", methods=["POST", "GET"])
def submit_form():
    """Form submission"""

    data = request.form.to_dict()
    name = request.form["username"]

    sender_name = request.form.get("username")
    sender_email = request.form.get("email")
    subject = request.form.get("subject")
    message = request.form.get("message")

    if request.method == "POST":
        try:
            # Save contact message in .csv file:
            write_to_csv(data)

            # Send me an email containing form data:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(user=my_user, password=my_password)
            server.sendmail(
                my_user,
                "tareq.joudeh@gmail.com",
                f"Subject: New message from your portfolio\n\n"
                f"Sender Name: {sender_name}\n"
                f"Sender Email: {sender_email}\n\n"
                f"Subject: {subject}\n"
                f"\n\n{message}".encode("utf8")
            )

        except:
            return "Error saving to .csv file."
        else:
            return render_template("thankyou.html", name=name, year=year)

    else:
        return "Error submitting form."


def write_to_csv(data):
    """Saving form data to a .csv file"""
    with open("database.csv", newline="\n", mode="a") as database:
        name = data["username"]
        email = data["email"]
        subject = data["subject"]
        message = data["message"]

        csv_writer = csv.writer(
            database,
            delimiter=" ",
            quotechar=" ",
            quoting=csv.QUOTE_MINIMAL,
        )

        csv_writer.writerow(
            [
                name,
                email,
                subject,
                message,
                """
                """
            ]
        )


if __name__ == '__main__':
    app.run()
