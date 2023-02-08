from flask import Flask, request, render_template
import db_processing

app = Flask(__name__)


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
        vacancy_data = {'user_id': 1,
                        'creation_date': '07.02.2023',
                        'position_name': position_name,
                        'company': company,
                        'description': description,
                        'contacts_ids': contacts_ids,
                        'comment': comment,
                        }
        db_processing.insert_info('vacancy', vacancy_data)

    result = db_processing.select_info("SELECT * FROM vacancy")
    return render_template('vacancy_add.html', vacancies=result)


@app.route('/vacancy/<int:vacancy_id>/', methods=['GET', 'PUT', 'DELETE'])
def vacancy_single(vacancy_id):
    result = db_processing.select_info(f"SELECT * FROM vacancy WHERE id == {vacancy_id}")
    return render_template('single.html', object=result)


@app.route('/vacancy/<int:vacancy_id>/events/', methods=['GET', 'POST'])
def vacancy_events(vacancy_id):
    if request.method == 'POST':
        description = request.form.get('description')
        event_date = request.form.get('event_date')
        title = request.form.get('title')
        due_to_date = request.form.get('due_to_date')
        event_data = {
            'vacancy_id': vacancy_id,
            'description': description,
            'event_date': event_date,
            'title': title,
            'due_to_date': due_to_date,
            'status': 0,
        }
        db_processing.insert_info('event', event_data)

    result = db_processing.select_info(f"SELECT * FROM event WHERE vacancy_id == {vacancy_id}")
    return render_template('event_add.html', events=result, vacancy_id=vacancy_id)


@app.route('/vacancy/<int:vacancy_id>/events/<int:event_id>/', methods=['GET', 'PUT', 'DELETE'])
def vacancy_event_single(vacancy_id, event_id):
    result = db_processing.select_info(f"SELECT * FROM event WHERE id == {event_id}")
    return render_template('single.html', object=result)


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
