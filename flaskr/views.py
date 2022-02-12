from flask import Blueprint, render_template, url_for

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/about')
def about():
    return render_template("about.html")

@views.route('/pricing')
def pricing():
    return render_template("pricing.html")

@views.route('/services')
def services():
    return render_template("services.html")
@views.route('/contact')
def contact():
    return render_template("contact.html")

