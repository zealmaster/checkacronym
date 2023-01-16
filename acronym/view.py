from flask import Flask, render_template, Blueprint, flash, request, redirect, session, url_for
from flask_login import login_required, current_user
from .model import Users, Create, Contribute
from . import db
import base64

view = Blueprint('view', __name__, url_prefix='/')
globals()


@view.route('/')
def index():
    search = Users.query.all()
    # query the Create table for list of all the acronyms
    acronym_added = Create.query.all()
    collect_acronym = {}
    for value in acronym_added:
        author = value.author_id
        # Look up the author of the acronym in the Users table
        added = Users.query.filter_by(id=author)
        for id in added:
            added_by = id
        # Sort the acronym by subject
        if value.subject not in collect_acronym:
            collect_acronym.update({value.subject: [value.acronym]})
        else:
            collect_acronym[value.subject].append(value.acronym)

    return render_template("base.html", search=search, user=current_user, acronym_added=acronym_added,
                           added_by=added_by, collect_acronym=collect_acronym)


# Pass stuff to Navbar
@view.context_processor
def base():
    acronym_added = Create.query.all()
    collect_acronym = {}
    for value in acronym_added:
        author = value.author_id
        added = Users.query.filter_by(id=author)
        for id in added:
            added_by = id
        if value.subject not in collect_acronym:
            collect_acronym.update({value.subject: [value.acronym]})
        else:
            collect_acronym[value.subject].append(value.acronym)
    return dict(added_by=added_by, collect_acronym=collect_acronym, user=current_user)


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
        other = request.form.get('others').capitalize()
        meaning = request.form.get('meaning').capitalize()
        definition = request.form.get('definition')

        if other == None:
            create_new = Create(acronym=abbreviation, subject=subject, meaning=meaning, definition=definition,
                                author_id=current_user.id)
            db.session.add(create_new)
            db.session.commit()
        else:
            create_new = Create(acronym=abbreviation, subject=other, meaning=meaning, definition=definition,
                                author_id=current_user.id)
            db.session.add(create_new)
            db.session.commit()

        flash("Your submission was successful")
    return render_template("create.html", user=current_user)


@view.route('/search', methods=['GET', 'POST'])
def search():
    search_list = []
    if request.method == 'POST':
        search_item = request.form.get('search').upper()
        search_for = Create.query.filter_by(acronym=search_item)
        for value in search_for:
            search_list.append(value)

    return render_template("search.html", user=current_user, search=search_list)


@view.route('/display_acronym/<int:id>', methods=['GET', 'POST'])
def display_acronym(id):
    # id = base64.b64decode(id)
    contributor_dict = []
    read_acronym = Create.query.filter_by(id=id).first()
    author = read_acronym.author_id

    added = Users.query.filter_by(id=author)
    for name in added:
        added_by = name
    read_contribution = Contribute.query.filter_by(original_author=read_acronym.id).all()
    for contributors in read_contribution:
        contributor = Users.query.filter_by(id=contributors.contributor_id).all()
        for i in contributor:
            contributor_dict.append(i)

    return render_template("display_acronym.html", user=current_user, added_by=added_by, search=read_acronym,
                           read_contribution=read_contribution, contributor_dict=contributor_dict)


@view.route('/profile/<int:id>', methods=['GET', 'POST'])
@login_required
def profile(id):
    fetch_profile = Users.query.filter_by(id=id).first()

    return render_template("profile.html", profile=fetch_profile, user=current_user)


@view.route('/contribute/<int:id>', methods=['GET', 'POST'])
@login_required
def contribute(id):
    fetch_acronym = Create.query.filter_by(id=id).first()
    if request.method == 'POST':
        original_author = fetch_acronym.id
        contributor_id = current_user.id
        contribution = request.form.get('contribution')
        contribute_now = Contribute(original_author=original_author, contributor_id=contributor_id,
                                    contribution=contribution)
        db.session.add(contribute_now)
        db.session.commit()
        flash("Your submission was successful")

    return render_template("contribute.html", user=current_user)
