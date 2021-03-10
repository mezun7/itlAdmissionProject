from itlAdmissionProject.settings import MAIN_HOST


def get_register_mail(email, username, password, activation_key):
    email_subject = 'Подтверждение пользователя в система регистрации IT-лицея КФУ'
    email_body = f'''Здравствуйте! " 
                 "Вы регистрировались в системе отбора в IT-лицей КФУ. " 
                 "Ваш логин: {username}" 
                 "Ваш пароль: {password}" 
                 "Спасибо за регистрацию. Чтобы активировать ваш пользователь, перейдите по ссылке ниже в течение 48 
часов {MAIN_HOST}/activate/{activation_key} 
         '''
    return email_subject, email_body
