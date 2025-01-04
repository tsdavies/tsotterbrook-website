import os
from flask import render_template, request, redirect, url_for, flash
from flask_mail import Message
from app.extensions import mail


def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        msg = Message(
            subject=f"New Contact Form Submission from {name}",
            sender=os.environ.get("MAIL_USERNAME"),  # Sender email from environment
            recipients=[os.environ.get("MAIL_USERNAME")],  # Send to yourself
            body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
        )
        try:
            mail.send(msg)
            flash(f"Thank you, {name}. Your message has been sent!", "success")
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")
            return redirect(url_for("contact"))

    return render_template("contact.html", title="Contact Me")
