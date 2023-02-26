from django.template.loader import render_to_string

from itlAdmissionProject.settings import MAIN_HOST, DOMAIN, PROTOCOL

templates_statuses = {
    'A': 'moderator/email_templates/accept.html',
    'A_10': 'moderator/email_templates/accept_10.html',
    'R': 'moderator/email_templates/reject.html'
}


def get_template(status, participant):
    if status == 'A' and participant.grade.number == 10:
        return templates_statuses['A_10']
    return templates_statuses[status]


def get_email_body(status, reason, participant):
    template = get_template(status, participant)
    email_body = render_to_string(template, {
        'reason': reason,
        'exam_date': participant.first_tour_register_date
    })
    return email_body


def get_moderator_mail(status, reason, participant):
    email_subject = 'Подтверждение пользователя в системе регистрации СУНЦ IT-лицея КФУ'
    email_body = get_email_body(status, reason, participant)

    return email_subject, email_body
