from django import forms
from django.contrib.auth import forms as fr, password_validation
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput, TextInput, PasswordInput, EmailInput, RadioSelect, Select, DateInput, \
    CheckboxInput, Textarea

from admission.models import File, Participant, GENDER_CHOICES, Group


class AuthForm(fr.AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': '', 'placeholder': 'Логин'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Пароль'}))

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        try:
            user = User.objects.get(username__exact=username)
            if not user.is_active:
                raise ValidationError('Подтвердите свой email, перейдя по ссылке в письме.')
            return username
        except User.DoesNotExist:
            raise ValidationError('Неверный логин или пароль.')


class PasswordResetForm(fr.PasswordResetForm):
    email = forms.EmailField(widget=EmailInput(attrs={
        'placeholder': 'Введите email'
    }
    ))


class SetPasswordForm(fr.SetPasswordForm):
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'placeholder': 'Введите новый пароль'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Введите повторно новый пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'placeholder': 'Повторно введите новый пароль'}),
    )


class RegisterForm(forms.ModelForm):
    repassword = forms.CharField(max_length=200, widget=PasswordInput(attrs={'placeholder': 'Повторно введите пароль'}))
    # grade_to_enter = forms.ChoiceField(required=True, choices=((group.number, group.number) for group in Group.objects.all().order_by('number')), widget=Select())
    grade_to_enter = forms.ModelChoiceField(required=True, queryset=Group.objects.all().order_by('number'),
                                            widget=Select())

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        widgets = {
            'username': TextInput(attrs={
                'placeholder': 'Логин',
            }),
            'password': PasswordInput(attrs={
                'placeholder': 'Пароль'
            }),
            'email': EmailInput(attrs={
                'placeholder': 'Адрес электронной почты'
            })
        }

    def clean_repassword(self):
        repassword = self.cleaned_data.get("repassword", "")
        password = self.cleaned_data.get("password", "")
        if repassword != password:
            raise ValidationError("Пароли не совпадают")
        return repassword

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        try:
            u = User.objects.get(email=email)
            raise ValidationError("Пользователь с таким адресом существует")
        except User.DoesNotExist:
            return email

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        try:
            u = User.objects.get(username=username)
            raise ValidationError("Пользователь с таким логином существует")
        except User.DoesNotExist:
            return username


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file',)


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ('portfolio_text',)

        widgets = {
            'portfolio_text': Textarea(attrs={
                'placeholder': "Список дипломов"
                # 'class': 'form-control'
            }),
        }


# class FileUpload(forms.ModelForm):
#     class Meta:
#         model = File
#         fields = ['file']
#         widgets = {
#             'file': ClearableFileInput(attrs={
#                 'multiple': True,
#                 'accept': '.csv'
#             })
#
#         }


class ChildInfo(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        participant = kwargs.pop('participant') # type: Participant
        print(participant)
        super(ChildInfo, self).__init__(*args, **kwargs)
        print(self.fields['gender'])
        ignored_fileds = ['fio_mother', 'fio_father', 'phone_mother', 'phone_father', 'out_of_competition',
                         'portfolio_text', 'birthday']
        self.fields['gender'].empty_label = "Укажите пол"
        if not participant.grade.have_profile:
            self.fields.pop('profile')
            ignored_fileds.append('profile')
        for k, v in self.fields.items():
            if k not in ignored_fileds:
                v.required = True

    class Meta:
        model = Participant
        # fileds = ['last_name', 'first_name', 'fathers_name', 'gender' ,'birthday', 'place_of_birth', 'phone_party',
        # 'school', 'grade']
        exclude = ['reg_status', 'activation_key', 'key_expires', 'portfolio', 'grade', 'user', 'portfolio_text',
                   'moderator', 'date_privilege_check', 'privilege_status']

        widgets = {
            'last_name': TextInput(attrs={
                'placeholder': 'Фамилия абитуриента',
                # 'required': 'True'
            }),
            'first_name': TextInput(attrs={
                'placeholder': 'Имя абитуриента',
            }),
            'fathers_name': TextInput(attrs={
                'placeholder': 'Отчество абитуриента',
            }),
            'gender': Select(attrs={
                'placeholder': 'Пол абитуриента',
                # 'class': 'form-control'
            }),
            'birthday': DateInput(format="%d.%m.%Y", attrs={
                'placeholder': "Дата рождения: дд.мм.гггг"
                # 'class': 'form-control'
            }),
            'place_of_birth': TextInput(attrs={
                'placeholder': "Место рождения"
                # 'class': 'form-control'
            }),
            'phone_party': TextInput(attrs={
                'placeholder': "Телефон абитуриента в формате: +7 (999) 999-99-99"
                # 'class': 'form-control'
            }),
            'school': TextInput(attrs={
                'placeholder': "Полное наименование образовательного учреждения по Уставу."
                # 'class': 'form-control'
            }),
            'lives': TextInput(attrs={
                'placeholder': "Город проживания с указанием региона"
                # 'class': 'form-control'
            }),
            'fio_mother': TextInput(attrs={
                'placeholder': "ФИО мамы"
                # 'class': 'form-control'
            }),
            'fio_father': TextInput(attrs={
                'placeholder': "ФИО отца"
                # 'class': 'form-control'
            }),
            'phone_mother': TextInput(attrs={
                'placeholder': "Телефон мамы в формате: +7 (999) 999-99-99"
                # 'class': 'form-control'
            }),
            'phone_father': TextInput(attrs={
                'placeholder': "Телефон отца в формате: +7 (999) 999-99-99"
                # 'class': 'form-control'
            }),
            'out_of_competition': CheckboxInput(attrs={
                'placeholder': "Есть ли у вас "
                # 'class': 'form-control'
            }),
        }

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name", "")
        return " ".join([el.capitalize() for el in last_name.split()])

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name", "")
        return " ".join([el.capitalize() for el in first_name.split()])

    def clean_fathers_name(self):
        fathers_name = self.cleaned_data.get("fathers_name", "")
        return " ".join([el.capitalize() for el in fathers_name.split()])

    def clean_fio_mother(self):
        fio_mother = self.cleaned_data.get("fio_mother", "")
        fio_father = self.cleaned_data.get("fio_father", "")
        return " ".join([el.capitalize() for el in fio_mother.split()])

    def clean_fio_father(self):
        fio_father = self.cleaned_data.get("fio_father", "")
        return " ".join([el.capitalize() for el in fio_father.split()])

    def clean_phone_mother(self):
        phone_mother = self.cleaned_data.get('phone_mother', '')
        phone_father = self.cleaned_data.get('phone_father', '')
        return phone_mother
