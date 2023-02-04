from flask import Flask
import app_data

app = Flask(__name__)


@app.route('/vacancy/', methods=['GET', 'POST'])
def all_vacancies():
    return app_data.vacancy_data


@app.route('/vacancy/<vacancy_id>/', methods=['GET', 'PUT', 'DELETE'])
def vacancy_single(vacancy_id):
    for vacancy in app_data.vacancy_data:
        if vacancy['id'] == vacancy_id:
            return vacancy


@app.route('/vacancy/<vacancy_id>/events/', methods=['GET', 'POST'])
def vacancy_events(vacancy_id):
    event_list = []
    for event in event_list:
        if event['vacancy_id'] == vacancy_id:
            event_list.append(event)

    return event_list


@app.route('/vacancy/<vacancy_id>/events/<event_id>/', methods=['GET', 'PUT', 'DELETE'])
def vacancy_event_single(event_id):
    for event in app_data.event_data:
        if event['id'] == event_id:
            return event


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
