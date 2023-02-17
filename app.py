from flask import Flask, request, render_template
import al_db
import models

app = Flask(__name__)

user_id = 1


@app.route('/', methods=['GET'])
def main_page():
    return render_template('main.html')


@app.route('/vacancy/', methods=['GET', 'POST'])
def all_vacancies():
    if request.method == 'POST':
        position_name = request.form.get('position_name')
        company = request.form.get('company')
        description = request.form.get('description')
        contacts_ids = request.form.get('contacts_ids')
        comment = request.form.get('comment')

        current_vacancy = models.Vacancy(position_name, company, description, contacts_ids, comment, 1, 1)
        al_db.db_session.add(current_vacancy)
        al_db.db_session.commit()

    result = al_db.db_session.query(models.Vacancy).all()
    return render_template('vacancy_add.html', vacancies=result)


@app.route('/vacancy/<int:vacancy_id>/', methods=['GET', 'POST'])
def vacancy_single(vacancy_id):
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
    return render_template('vacancy_single.html', object=result)


@app.route('/vacancy/<int:vacancy_id>/events/', methods=['GET', 'POST'])
def vacancy_events(vacancy_id):
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
    return 'vacancy history'


@app.route('/user/', methods=['GET'])
def user():
    return 'user\'s page'


@app.route('/user/calendar/', methods=['GET'])
def user_calendar():
    return 'user\'s calendar'


@app.route("/user/mail/", methods=['GET', 'PUT'])
def user_mail():
    return 'user\'s mail'


@app.route("/user/settings/", methods=['GET', 'PUT'])
def user_settings():
    return 'user\'s settings'


@app.route("/user/documents/", methods=['GET', 'POST'])
def user_documents():
    return 'user\'s documents'


@app.route("/user/templates/", methods=['GET', 'POST'])
def user_templates():
    return 'user\'s templates'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
