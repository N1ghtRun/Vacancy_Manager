from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from datetime import datetime
from al_db import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    name = Column(String(50), nullable=False)
    login = Column(String(50), unique=True, nullable=False)
    password = Column(String(24), nullable=False)
    email = Column(String(120), unique=True, nullable=False)

    def __init__(self, name, login, password, email):
        self.name = name
        self.login = login
        self.password = password
        self.email = email

    def __repr__(self):
        return f'user {self.name}'


class EmailCreds(Base):
    __tablename__ = 'email_creds'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    login = Column(String(50), unique=True, nullable=False)
    password = Column(Text(24), nullable=False)
    pop_server = Column(Text(120))
    smtp_server = Column(Text(120))

    def __init__(self, user_id, email, login, password, pop_server, smtp_server):
        self.user_id = user_id
        self.email = email
        self.login = login
        self.password = password
        self.pop_server = pop_server
        self.smtp_server = smtp_server


class Vacancy(Base):
    __tablename__ = 'vacancy'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    creation_date = Column(DateTime, default=datetime.utcnow())
    status = Column(Integer, nullable=False, default=0)
    company = Column(String(120), nullable=False)
    contacts_ids = Column(String(16))
    description = Column(Text, nullable=False)
    position_name = Column(String(50), nullable=False)
    comment = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, position_name, company, description, contacts_ids, comment, status, user_id):
        self.position_name = position_name
        self.company = company
        self.description = description
        self.contacts_ids = contacts_ids
        self.comment = comment
        self.status = status
        self.user_id = user_id

    def __repr__(self):
        return f'vacancy {self.position_name}'


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    vacancy_id = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    event_date = Column(String(10), nullable=False)
    title = Column(String(50), nullable=False)
    due_to_date = Column(String(10), nullable=False)
    status = Column(Integer, nullable=False, default=0)

    def __init__(self, vacancy_id, description, event_date, title, due_to_date, status):
        self.vacancy_id = vacancy_id
        self.description = description
        self.event_date = event_date
        self.title = title
        self.due_to_date = due_to_date
        self.status = status

    def __repr__(self):
        return f'event {self.title}'


class Contacts(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    name = Column(String(50), nullable=0)

    def __init__(self, name):
        self.name = name


class Documents(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    name = Column(String(50), nullable=0)
    description = Column(Text)
    content = Column(Text, nullable=False)

    def __init__(self, user_id, name, description, content):
        self.user_id = user_id
        self.name = name
        self.description = description
        self.content = content


class Templates(Base):
    __tablename__ = 'templates'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    name = Column(Text, nullable=False)
    content = Column(Text, nullable=False)

    def __init__(self, user_id, name, content):
        self.user_id = user_id
        self.name = name
        self.content = content
