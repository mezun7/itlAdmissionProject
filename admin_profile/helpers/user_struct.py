import hashlib

from first_tour.models import TourParticipantScan, Tour, ExamResult, UserAppeal, ExamSheetScan
from itlAdmissionProject.settings import SALT


class ListStruct:
    participant = None
    exam_result = None
    appeal = None
    scan: str = None

    def __init__(self, participant):
        self.participant = participant
        self.exam_result = ExamResult.objects.filter(participant=participant).order_by('exam_subject__ordering')
        try:
            self.appeal = UserAppeal.objects.filter(participant=participant).order_by('-id')[0]
        except:
            self.appeal = None
        if len(self.exam_result) > 0:
            self.scan = get_scans(participant, self.exam_result.first().exam_subject.tour)


def get_scans(participant, tour):
    try:
        scan = ExamSheetScan.objects.filter(
            tour_order=tour.tour_order, participant=participant
        ).order_by('-id')[0]
        return scan
        # scan_user = TourParticipantScan.objects.get(participant=participant, tour=tour)
        # fl_name = SALT + scan_user.scan_file_name.split('.')[0]
        # scan_file = str(hashlib.sha256(fl_name.encode('utf-8')).hexdigest()) + '.zip'
        # return scan_file

    except:
        return None
