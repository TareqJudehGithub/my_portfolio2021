import csv
import os
import smtplib
from datetime import datetime

from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import EmailField

# Flask instance
app = Flask(__name__)

# Constants:
year = datetime.now().year

# Gmail credentials:
my_user = os.environ.get("EMAIL_USER")
my_password = os.environ.get("EMAIL_PASS")

# Secret key
SECRET_KEY = os.environ.get("SECRET_KEY")
app.config["SECRET_KEY"] = SECRET_KEY


# Form class
class ContactForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    email = EmailField("email",
                       validators=[DataRequired(), Email()])
    subject = StringField("subject", validators=[
        DataRequired("Please enter a title for your message.")])
    message = TextAreaField("message", validators=[
        DataRequired("Please leave me a message here :)")])
    submit = SubmitField("Submit")


@app.route('/')
def hello_world():
    """Main page"""
    return render_template("index.html", year=year)


@app.route("/<string:page_name>")
def html_page(page_name):
    """Accessing portfolio HTML pages"""
    return render_template(page_name, year=year)


@app.route("/submit_form", methods=["GET", "POST"])
def submit_form():
    """Form submission"""

    # wtf_form constants:
    form_name = None
    form = ContactForm()

    # Submit form:
    try:
        if form.validate_on_submit():

            # Form fields:
            form_name = form.name.data
            form.name.data = ""
            form_email = form.email.data
            form.email.data = ""

            form_subject = form.subject.data
            form.subject.data = ""

            form_message = form.message.data
            form.message.data = ""

            # post form data to file database.csv:
            data = request.form.to_dict()
            write_to_csv(data)

            # Send me emails from contacts:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(user=my_user, password=my_password)
            server.sendmail(
                from_addr=my_user,
                to_addrs="tareq.joudeh@gmail.com",
                msg=f"Subject: New message from your portfolio\n\n"
                    f"Sender Name: {form_name}\n"
                    f"Sender Email: {form_email}\n"
                    f"Subject: {form_subject}\n"
                    f"\n{form_message}".encode("utf8")
            )

    except:
        return "Error while trying posting form data."

    else:
        return render_template(
            "contact_me.html",
            name=form_name,
            form=form,
            year=year
        )


@app.route("/wtf_thankyou")
def wtf_thank_you():
    return render_template("wtf_thankyou.html")


def write_to_csv(data):
    """Saving form data to a .csv file"""
    with open("database.csv", newline="\n", mode="a") as database:
        name = data["name"]
        email = data["email"]
        subject = data["subject"]
        message = data["message"]

        csv_writer = csv.writer(
            database,
            delimiter="\n",
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


# Error route:
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", error=error), 404


if __name__ == '__main__':
    app.run()

