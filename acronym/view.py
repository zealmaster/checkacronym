from flask import Flask, render_template, Blueprint, flash, request, redirect, session, url_for
from flask_login import login_required, current_user
from .model import Users, Create
from . import db
import base64

view = Blueprint('view', __name__, url_prefix='/')


@view.route('/')
def index():
    search = Users.query.all()
    acronym_added = Create.query.all()
    for value in acronym_added:
        author = value.author_id
        added = Users.query.filter_by(id=author)
        for id in added:
            added_by = id
    return render_template("base.html", search=search, user=current_user, acronym_added=acronym_added,
                           added_by=added_by)


@view.route('/home')
@login_required
def home():
    search = Users.query.all()
    return render_template("index.html", search=search, user=current_user)


@view.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        abbreviation = request.form.get('acronym').upper()
        subject = request.form.get('subject')
        meaning = request.form.get('meaning').capitalize()
        definition = request.form.get('definition')

        create_new = Create(acronym=abbreviation, subject=subject, meaning=meaning, definition=definition,
                            author_id=current_user.id)
        db.session.add(create_new)
        db.session.commit()
        flash("Your submission was successful")
    return render_template("create.html", user=current_user)


@view.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_item = request.form.get('search').upper()
        search_for = Create.query.filter_by(acronym=search_item)
        search_for = Create.filter(acronym=search_item)
        for value in search_for:
            if search_item != value.acronym:
                flash('No result found')
                break
            author = value.author_id
            added = Users.query.filter_by(id=author)
            for name in added:
                added_by = name
        flash('No result found')

    return render_template("search.html", user=current_user, search=search_for, added_by=added_by)


@view.route('/display_acronym/<int:id>', methods=['GET', 'POST'])
def display_acronym(id):
    # id = base64.b64decode(id)
    read_for = Create.query.filter_by(id=id).first()
    author = read_for.author_id

    added = Users.query.filter_by(id=author)
    for name in added:
        added_by = name

    return render_template("display_acronym.html", user=current_user, added_by=added_by, search=read_for)
