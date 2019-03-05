import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request, url_for

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    # validate a form submission
    print(request.form)
    for key, value in (request.form).items():
        if value is '' and key is not 'other':
            return render_template("error.html", message="Insufficient data entered")
    if 'sport' not in (request.form).keys():
        return render_template("error.html", message="Insufficient data entered")

    # write the form to a new row in CSV
    with open('survey.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(list(request.form.values()))
    # redirect user to /sheet
    return redirect(url_for('.get_sheet'))


@app.route("/sheet", methods=["GET"])
def get_sheet():
    with open('survey.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        details = list(reader)
        print(details)
    return render_template("sheet.html", details=details)
