import os
from app.extensions import mail
from flask import render_template, render_template_string, request, redirect, url_for, flash
from app.models import db, User, BlogPost, Comment
from app.forms import LoginForm, RegisterForm, BlogPostForm, CommentForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from app.pokemon_utils import pokemon_color


def init_routes(app):
    @app.route('/')
    @app.route('/about')
    def about():
        return render_template('about.html', title="About Me")

    @app.route('/pokemon', methods=['GET', 'POST'])
    def pokemon():
        import requests
        data = None

        if request.method == 'POST':
            name = request.form.get('name')
            response = requests.get(
                f'https://pokeapi.co/api/v2/pokemon/{name.lower()}')

            if response.ok:
                data = response.json()
                data["types"] = [t["type"]["name"] for t in data["types"]]
                data["color"] = pokemon_color(data["types"])

        return render_template('pokemon.html', data=data, title="Pokémon Search")

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')

            msg = Message(
                subject=f"New Contact Form Submission from {name}",
                # Sender email from env
                sender=os.environ.get('MAIL_USERNAME'),
                # Send to yourself
                recipients=[os.environ.get('MAIL_USERNAME')],
                body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            )
            try:
                mail.send(msg)
                flash(
                    f"Thank you, {name}. Your message has been sent!", "success")
            except Exception as e:
                flash(f"An error occurred: {str(e)}", "danger")

            return redirect(url_for('about'))

        return render_template('contact.html', title="Contact Me")

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password, form.password.data):
                flash('Login successful!', 'success')
                return redirect(url_for('about'))
            else:
                flash('Invalid email or password', 'danger')
        return render_template('login.html', form=form, title="Login")

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            if User.query.filter_by(email=form.email.data).first():
                flash('Email already registered', 'danger')
                return redirect(url_for('register'))
            # Use pbkdf2:sha256 for hashing
            hashed_password = generate_password_hash(
                form.password.data, method='pbkdf2:sha256')
            new_user = User(username=form.username.data,
                            email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', form=form, title="Register")

    @app.route('/blog')
    def blog():
        posts = BlogPost.query.order_by(BlogPost.timestamp.desc()).all()
        return render_template('blog.html', posts=posts)

    @app.route('/blog/<int:post_id>', methods=['GET', 'POST'])
    def post_detail(post_id):
        post = BlogPost.query.get_or_404(post_id)
        form = CommentForm()
        if form.validate_on_submit():
            comment = Comment(
                content=form.content.data,
                author=form.author.data,
                post_id=post.id  # Ensure post_id is set
            )
            db.session.add(comment)
            db.session.commit()
            flash('Comment added!', 'success')
            return redirect(url_for('post_detail', post_id=post_id))
        return render_template('post_detail.html', post=post, form=form)

    @app.route('/blog/new', methods=['GET', 'POST'])
    def new_post():
        form = BlogPostForm()
        if form.validate_on_submit():
            post = BlogPost(title=form.title.data,
                            content=form.content.data, author=form.author.data)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', 'success')
            return redirect(url_for('blog'))
        return render_template('new_post.html', form=form)

    @app.route('/blog/<int:post_id>/edit', methods=['GET', 'POST'])
    def edit_post(post_id):
        post = BlogPost.query.get_or_404(post_id)
        form = BlogPostForm(obj=post)
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            post.author = form.author.data
            db.session.commit()
            flash('Post updated successfully!', 'success')
            return redirect(url_for('post_detail', post_id=post.id))
        return render_template('new_post.html', form=form, post=post, edit=True)

    @app.route('/blog/<int:post_id>/delete', methods=['POST', 'GET'])
    def delete_post(post_id):
        post = BlogPost.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!', 'success')
        return redirect(url_for('blog'))

    @app.route('/comment/<int:comment_id>/delete', methods=['POST', 'GET'])
    def delete_comment(comment_id):
        comment = Comment.query.get_or_404(comment_id)
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted successfully!', 'success')
        return redirect(request.referrer or url_for('blog'))
