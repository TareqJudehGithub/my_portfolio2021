from flask import Flask, render_template, request
from datetime import datetime
import csv

year = datetime.now().year
app = Flask(__name__)


@app.route('/')
def hello_world():
    """Main page"""
    return render_template("index.html",year=year)


@app.route("/<string:page_name>")
def html_page(page_name):
    """Accessing portfolio HTML pages"""
    return render_template(page_name, year=year)


@app.route("/submit_form", methods=["POST", "GET"])
def submit_form():
    """Form submission"""
    if request.method == "POST":
        try:
            data = request.form.to_dict()
            name = request.form["username"]

            write_to_csv(data)

            return render_template("thankyou.html", name=name, year=year)

        except:
            return "Error saving to .csv file."

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

