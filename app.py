from flask import Flask, flash, request, render_template, url_for, redirect
from flask import session

import al_db
import mongo_db
from bson.objectid import ObjectId
import email_lib
import models
import celery_worker

app = Flask(__name__)
app.secret_key = 'super secret key'

user_id = 1


@app.route('/', methods=['GET', 'POST'])
def main_page():
    current_user = session.get('user_name', None)
    if current_user is None:
        return redirect(url_for('login'))
    return render_template('main.html', user_name=current_user)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == '' or password == '':
            redirect(url_for('login'))

        user = al_db.db_session.query(models.User).filter(models.User.login == username).first()
        if user is None:
            return redirect(url_for('login'))
        if user.password != password:
            return redirect(url_for('login'))
        session['user_id'] = user.id
        session['user_name'] = user.name

        return redirect(url_for('main_page'))

    return render_template('login.html')


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    if request.method == "POST":
        login = request.form.get('login')
        password = request.form.get('password')
        email = request.form.get('email')
        name = request.form.get('name')

        current_user = models.User(name, login, password, email)

        try:
            al_db.db_session.add(current_user)
            al_db.db_session.commit()
        except Exception as err:
            print(err)

    return render_template('registration.html', title='registration')


@app.route('/logout/', methods=['GET'])
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('main_page'))


@app.route('/vacancy/', methods=['GET', 'POST'])
def all_vacancies():
    if session.get('user_id', None) is None:
        return redirect(url_for('main_page'))
    if request.method == 'POST':
        position_name = request.form.get('position_name')
        company = request.form.get('company')
        description = request.form.get('description')
        comment = request.form.get('comment')
        contacts_name = request.form.get('contacts_name')
        contacts_email = request.form.get('contacts_email')
        contacts_phone = request.form.get('contacts_phone')
        contacts_messanger = request.form.get('contacts_messanger')

        # creating new document in MongoDB
        new_contact = {
            "name": contacts_name,
            "email": contacts_email,
            "phone": contacts_phone,
            "messanger": contacts_messanger,
            "test": "test"
        }
        # mongo_db.collection.insert_one(new_contact)
        contacts_id = str(mongo_db.collection.insert_one(new_contact).inserted_id)

        # adding new entry to PostgresDB
        current_vacancy = models.Vacancy(position_name, company, description, contacts_id, comment, 0,
                                         session.get('user_id'))
        al_db.db_session.add(current_vacancy)
        al_db.db_session.commit()

    result = al_db.db_session.query(models.Vacancy).filter(models.Vacancy.user_id == session.get('user_id'))
    return render_template('vacancy_add.html', vacancies=result)


@app.route('/vacancy/<int:vacancy_id>/', methods=['GET', 'POST'])
def vacancy_single(vacancy_id):
    if session.get('user_id', None) is None:
        return redirect(url_for('main_page'))
    if request.method == 'POST':
        position_name = request.form.get('position_name')
        status = request.form.get('status')
        company = request.form.get('company')
        description = request.form.get('description')
        contact_ids = request.form.get('contact_ids')
        comment = request.form.get('comment')

        al_db.db_session.query(models.Vacancy).filter(models.Vacancy.id == vacancy_id).update(
            {models.Vacancy.position_name: position_name,
             models.Vacancy.status: status,
             models.Vacancy.company: company,
             models.Vacancy.description: description,
             models.Vacancy.contacts_ids: contact_ids,
             models.Vacancy.comment: comment,
             }, synchronize_session=False
        )
        al_db.db_session.commit()

    result = al_db.db_session.query(models.Vacancy).get(vacancy_id)
    contacts = []

    # contact's ID's in DB should be separated by a space(" ")
    ids = str(result.contacts_ids).split(" ")
    for item in ids:
        contact = mongo_db.collection.find_one({'_id': ObjectId(item)})
        contacts.append(contact)

    return render_template('vacancy_single.html', object=result, contacts=contacts)


@app.route('/vacancy/<int:vacancy_id>/events/', methods=['GET', 'POST'])
def vacancy_events(vacancy_id):
    if session.get('user_id', None) is None:
        return redirect(url_for('main_page'))
    if request.method == 'POST':
        description = request.form.get('description')
        event_date = request.form.get('event_date')
        title = request.form.get('title')
        due_to_date = request.form.get('due_to_date')

        current_event = models.Event(vacancy_id, description, event_date, title, due_to_date, 0)
        al_db.db_session.add(current_event)
        al_db.db_session.commit()

    result = al_db.db_session.query(models.Event).filter(models.Event.vacancy_id == vacancy_id)
    return render_template('event_add.html', events=result, vacancy_id=vacancy_id)


@app.route('/vacancy/<int:vacancy_id>/events/<int:event_id>/', methods=['GET', 'POST'])
def vacancy_event_single(vacancy_id, event_id):
    if session.get('user_id', None) is None:
        return redirect(url_for('main_page'))
    if request.method == 'POST':
        description = request.form.get('description')
        event_date = request.form.get('event_date')
        title = request.form.get('title')
        due_to_date = request.form.get('due_to_date')

        al_db.db_session.query(models.Event).filter(models.Event.id == event_id).update(
            {models.Event.vacancy_id: vacancy_id,
             models.Event.description: description,
             models.Event.event_date: event_date,
             models.Event.title: title,
             models.Event.due_to_date: due_to_date,
             models.Event.status: 0,
             }, synchronize_session=False
        )
        al_db.db_session.commit()

    result = al_db.db_session.query(models.Event).get(event_id)
    return render_template('event_single.html', object=result)


@app.route('/vacancy/<id>/history', methods=['GET'])
def vacancy_history():
    if session.get('user_id', None) is None:
        return redirect(url_for('main_page'))
    return 'vacancy history'


@app.route('/user_page/', methods=['GET'])
def user_page():
    if session.get('user_id', None) is None:
        return redirect(url_for('main_page'))
    return 'user\'s page'


@app.route('/user/calendar/', methods=['GET'])
def user_calendar():
    if session.get('user_id', None) is None:
        return redirect(url_for('main_page'))
    return 'user\'s calendar'


@app.route("/user/mail/", methods=['GET', 'POST'])
def user_mail():
    if session.get('user_id', None) is None:
        return redirect(url_for('main_page'))
    email_settings = al_db.db_session.query(models.EmailCreds).filter_by(user_id=session.get('user_id')).first()
    if email_settings is None:
        return 'no email creds for current user. You can set them on settings page'
    email_obj = email_lib.EmailWrapper(
        user_email=email_settings.email,
        login=email_settings.login,
        password=email_settings.password,
        smtp_server=email_settings.smtp_server,
        pop_server=email_settings.pop_server,
        imap_server=email_settings.imap_server,
        smtp_port=email_settings.smtp_port,
        pop_port=email_settings.pop_port,
        imap_port=email_settings.imap_port,
    )

    if request.method == 'POST':
        recipient = request.form.get('recipient_email')
        email_text = request.form.get('email_content')
        email_subject = request.form.get('email_subject')
        celery_worker.send_mail.apply_async(args=[email_settings.id, recipient, email_subject, email_text])
        return "email sent"

    if email_settings.imap_server and email_settings.imap_port:
        email_list = email_obj.imap_receiver()
    elif email_settings.pop_server and email_settings.pop_port:
        email_list = email_obj.pop3_receiver()
    else:
        email_list = None

    return render_template('mail.html', emails=email_list)


@app.route("/user/settings/", methods=['GET', 'POST'])
def user_settings():
    if session.get('user_id', None) is None:
        return redirect(url_for('main_page'))
    user_id = session.get('user_id')
    email_creds = al_db.db_session.query(models.EmailCreds).filter(models.EmailCreds.user_id == user_id).first()
    if request.method == 'POST':
        email = request.form.get('email')
        login = request.form.get('login')
        password = request.form.get('password')
        smtp_server = request.form.get('smtp_server')
        smtp_port = request.form.get('smtp_port')
        imap_server = request.form.get('imap_server')
        imap_port = request.form.get('imap_port')
        pop_server = request.form.get('pop_server')
        pop_port = request.form.get('pop_port')

        if email_creds is None:
            email_creds = models.EmailCreds(user_id, email, login, password, smtp_server, smtp_port, imap_server,
                                            imap_port, pop_server, pop_port)
            al_db.db_session.add(email_creds)
            al_db.db_session.commit()
        else:
            al_db.db_session.query(models.EmailCreds).filter(models.EmailCreds.user_id == user_id).update(
                {models.EmailCreds.email: email,
                 models.EmailCreds.login: login, }, synchronize_session=False)
            al_db.db_session.commit()

    return render_template('settings.html', email_creds=email_creds, title='Settings')


@app.route("/user/documents/", methods=['GET', 'POST'])
def user_documents():
    if session.get('user_id', None) is None:
        return redirect(url_for('main_page'))
    return 'user\'s documents'


@app.route("/user/templates/", methods=['GET', 'POST'])
def user_templates():
    if session.get('user_id', None) is None:
        return redirect(url_for('main_page'))
    return 'user\'s templates'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
