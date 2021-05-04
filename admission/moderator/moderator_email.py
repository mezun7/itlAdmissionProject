from django.template.loader import render_to_string

from itlAdmissionProject.settings import MAIN_HOST, DOMAIN, PROTOCOL

templates_statuses = {
    'A': 'moderator/email_templates/accept.html',
    'R': 'moderator/email_templates/reject.html'
}


def get_moderator_mail(status, reason, exam_date):
    email_subject = 'Подтверждение пользователя в системе регистрации IT-лицея КФУ'
    email_body = render_to_string(templates_statuses[status], {
        'reason': reason,
        'exam_date': exam_date
    })

    return email_subject, email_body
