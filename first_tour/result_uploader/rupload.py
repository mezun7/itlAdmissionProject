import csv

from admin_profile.models import Error
from admission.models import Participant


def upload(path, tour):
    from first_tour.models import ExamResult, TourParticipantScan
    with open(path) as File:
        reader = csv.DictReader(File)
        exam_subjects = tour.examsubject_set.all()
        subj = []
        print(subj)
        results = []
        scans = []

        for row in reader:
            na = False
            try:
                participant = Participant.objects.get(id=row['id'])
            except:
                print('help')
            for esubj in exam_subjects:
                exam_result = ExamResult()
                print(participant)
                exam_result.participant = participant
                if row[esubj.subject.name] != '#N/A':

                    exam_result.score = float(row[esubj.subject.name].replace(',', '.'))
                else:
                    na = True
                    exam_result.score = 0
                exam_result.exam_subject = esubj
                results.append(exam_result)
            tscan = TourParticipantScan()
            tscan.participant = participant
            tscan.tour = tour
            tscan.scan_file_name = row['blank']
            if not na:
                print('here')
                scans.append(tscan)

        ExamResult.objects.bulk_create(results)
        TourParticipantScan.objects.bulk_create(scans)

    # print(path, tour.name)


# if __name__ == '__main__':
#     from first_tour.models import Tour
#
#     upload('/Users/shuhrat/Downloads/results.csv', Tour.objects.get('2'))


def upload_next_tour_participants(path, tour):
    from first_tour.models import NextTourPass
    with open(path) as File:
        reader = csv.DictReader(File)
        results = []
        for row in reader:
            tmp = NextTourPass()
            tmp.tour = tour
            tmp.participant = Participant.objects.get(id=row['id'])
            tmp.type_of_pass = 'P'
            results.append(tmp)

        NextTourPass.objects.bulk_create(results)


def upload_liter(path, tour_ordering):
    from first_tour.models import LiterGrade

    with open(path) as File:
        reader = csv.DictReader(File)
        for row in reader:
            participant = Participant.objects.get(pk=row['id'])
            try:
                lg = LiterGrade.objects.get(tour__profile=participant.profile,
                                            tour__grade=participant.grade,
                                            tour__tour_order=tour_ordering,
                                            name=row['liter'])
                lg.participants.add(participant)
            except LiterGrade.DoesNotExist:
                error = Error()
                error.participant = participant
                error.message = 'Doesnt exists LiterGrade'
                error.save()

