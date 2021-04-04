from django.template.loader import render_to_string

from itlAdmissionProject.settings import MAIN_HOST, DOMAIN, PROTOCOL


def get_register_mail(username, activation_key):
    email_subject = 'Подтверждение пользователя в системе регистрации IT-лицея КФУ'
    email_body = render_to_string('registration/register_email_confirm.html', {
        'user': username,
        'activation_key2': activation_key,
        'domain': DOMAIN,
        'protocol': PROTOCOL
    })

    return email_subject, email_body
