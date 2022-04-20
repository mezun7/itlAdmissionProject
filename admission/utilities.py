from datetime import datetime, timedelta
import os


def is_tour_available(tour_date):
    n = 2
    deadline = tour_date - timedelta(days=n)  # закрыть регистрацию  за n дней
    return deadline >= datetime.now()


def file_add_extension(file_list):
    for v in file_list:
        # extension = list(os.path.splitext(v.file.name))[1]
        # v.file.extension = extension
        file_extension(v)


def file_extension(f):
    f.file.extension = list(os.path.splitext(f.file.name))[1]
