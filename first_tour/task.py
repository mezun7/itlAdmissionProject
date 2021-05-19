import logging
import time

from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from itlAdmissionProject.celery import app


@app.task
def test_celery(x):
    # print('Started----------------')
    i = 0
    time.sleep(10)
    f = open('/Users/shuhrat/PycharmProjects/itlAdmissionProject/tmp44.txt', 'w')
    # print('Done')
    f.close()
