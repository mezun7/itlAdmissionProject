from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput, TextInput, PasswordInput, EmailInput, RadioSelect, Select, DateInput, \
    CheckboxInput, Textarea

from admission.models import File, Participant, GENDER_CHOICES


class AuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': '', 'placeholder': 'Логин'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Пароль'}))


class RegisterForm(forms.ModelForm):
    repassword = forms.CharField(max_length=200, widget=PasswordInput(attrs={'placeholder': 'Повторно введите пароль'}))

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


class FileUpload(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={
                'multiple': True,
                'accept': '.csv'
            })

        }


class ChildInfo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChildInfo, self).__init__(*args, **kwargs)
        print(self.fields['gender'])
        self.fields['gender'].empty_label = "Укажите пол"

        for k, v in self.fields.items():
            if k not in ['fio_mother', 'fio_father', 'phone_mother', 'phone_father', 'out_of_competition', 'portfolio_text']:
                v.required = True

    tmp_field = forms.ChoiceField(choices=GENDER_CHOICES, widget=Select(attrs={'placeholder': 'Пол абитуриента'}))

    class Meta:
        model = Participant
        # fileds = ['last_name', 'first_name', 'fathers_name', 'gender' ,'birthday', 'place_of_birth', 'phone_party', 'school', 'grade']
        exclude = ['reg_status', 'activation_key', 'key_expires', 'portfolio']

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
            'birthday': DateInput(format="%d/%m/%Y", attrs={
                'placeholder': "Дата рождения: дд/мм/гггг"
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
                'placeholder': "Полное наименвоание образовательного учреждения по Уставу."
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
            'portfolio_text': Textarea(attrs={
                'placeholder': "Список дипломов"
                # 'class': 'form-control'
            }),
        }
