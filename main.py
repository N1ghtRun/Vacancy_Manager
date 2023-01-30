from flask import Flask

app = Flask(__name__)


@app.route('/vacancy/', methods=['GET', 'POST'])
def all_vacancies():
    return 'all vacancies'


# на занятті метод DELETE не був прописаний у аналогічній функції, але мені здається, що користувач має мати змогу
# видаляти як вакансії, так і їхні івенти
@app.route('/vacancy/<id>/', methods=['GET', 'PUT', 'DELETE'])
def vacancy_single():
    return 'single vacancy'


@app.route('/vacancy/<id>/events/', methods=['GET', 'POST'])
def vacancy_events():
    return 'all events'


@app.route('/vacancy/<id>/events/<event_id>/', methods=['GET', 'PUT', 'DELETE'])
def vacancy_event_single():
    return 'single event'


@app.route('/vacancy/<id>/history', methods=['GET'])
def vacancy_history():
    return 'vacancy history'


@app.route('/user/', methods=['GET'])
def user():
    return 'user\'s page'


@app.route('/user/calendar/', methods=['GET'])
def user_calendar():
    return 'user\'s calendar'


# PUT на випадок, якщо користувач захоче змінити свій mail
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
