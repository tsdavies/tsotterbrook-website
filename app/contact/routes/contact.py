import os
from flask import render_template, redirect, url_for, flash
from app.contact.forms.contact_form import ContactForm
from flask_mail import Message
from app.extensions import mail


def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message(
            subject=f"New Contact Form Submission from {form.name.data}",
            sender=form.email.data,
            recipients=[os.environ.get("MAIL_USERNAME")],
            body=form.message.data
        )
        mail.send(msg)
        flash("Your message has been sent successfully.", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html", form=form)