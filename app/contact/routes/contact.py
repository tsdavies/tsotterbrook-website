import os

import bleach
from flask import render_template, redirect, url_for, flash
from flask_mail import Message

from app.contact.forms.contact_form import ContactForm
from app.extensions import mail


def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Sanitize inputs
        sanitized_name = bleach.clean(form.name.data)
        sanitized_email = bleach.clean(form.email.data)
        sanitized_message = bleach.clean(form.message.data)

        msg = Message(
            subject=f"New Contact Form Submission from {sanitized_name}",
            sender=sanitized_email,
            recipients=[os.environ.get("MAIL_USERNAME")],
            body=sanitized_message,
        )
        mail.send(msg)
        flash("Your message has been sent successfully.", "success")
        return redirect(url_for("contact.contact"))
    return render_template("contact.html", form=form)
