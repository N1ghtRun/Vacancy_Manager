from celery import Celery
from email_lib import EmailWrapper
from models import EmailCreds
import al_db
import os


RABBIT_HOST = os.environ.get('RABBIT_HOST', 'localhost')

app = Celery('celery_worker', broker=f'pyamqp://guest:guest@{RABBIT_HOST}:5672//')


@app.task()
def send_mail(id_email_creds, recipient, subject, message):
    email_creds_detail = al_db.db_session.query(EmailCreds).get(id_email_creds)
    email_wrapper = EmailWrapper(**email_creds_detail.get_mandatory_fields())
    email_wrapper.send_email(recipient, subject, message)
