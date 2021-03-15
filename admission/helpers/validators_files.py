from django.core.exceptions import ValidationError

from itlAdmissionProject.settings import FILE_SIZE_LIMIT


def file_size(value):
    limit = FILE_SIZE_LIMIT
    limit_in_mb = FILE_SIZE_LIMIT / 1024 / 1024
    if value.size > limit:
        raise ValidationError(f'Файл слишком большой. Ограничение на файл - {limit_in_mb} МБ.')
