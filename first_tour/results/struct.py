import datetime

from admin_profile.helpers.user_struct import get_scans
from admission.models import Participant
from first_tour.forms import UserAppealForm, UserConfirmForm
from first_tour.models import ExamResult, Tour, UserAppeal, TourParticipantScan, NextTourPass, UploadConfirm
from first_tour.models import ExamSheetScan

def get_final_result_release_date(final_result_release_date):
    return False if final_result_release_date is None else datetime.datetime.now() > final_result_release_date


class ResultParticipant:
    result = None
    passing_type = None
    result_release_date = None
    final_result_release_date = None
    scan = None
    score = None
    portfolio_score = 0
    tour = None
    form = None
    apeal_application = False
    participant: Participant = None
    final_apply_form = None

    def get_passing_type(self):
        try:
            if self.tour.final_result_release_date is None:
                return None
            if self.tour.final_result_release_date > datetime.datetime.now():
                return None
            return NextTourPass.objects.get(tour=self.tour, participant=self.participant).type_of_pass
        except:
            return None

    def get_form(self):
        participant = self.participant

        try:
            UserAppeal.objects.get(participant=participant, tour=self.tour)
            self.apeal_application = True
            return None
        except UserAppeal.DoesNotExist:
            if self.tour.appeal_application_end_date < datetime.datetime.now():
                return None
            return UserAppealForm(initial={
                'tour': self.tour,
                'participant': self.participant
            })

    def get_final_form(self):
        if self.passing_type is None:
            return None
        try:
            uconfirm = UploadConfirm.objects.get(participant=self.participant, tour=self.tour)
            return None
        except:
            form = UserConfirmForm(initial={
                'tour': self.tour,
                'participant': self.participant
            })
            return form

    def get_final_score(self):
        score = self.portfolio_score
        for subject in self.result:

            score += subject.score
            if subject.appeal_score is not None:
                score += subject.appeal_score
        return score

    def get_scan(self):
        try:
            scan = ExamSheetScan.objects.filter(
                tour_order=self.tour.tour_order, participant=self.participant
            ).order_by('-id')[0]
            return scan
            # return TourParticipantScan.objects.get(tour=self.tour,
            #                                        participant=self.participant).scan_file_name
        except:
            return None

    def __init__(self, result, result_release_date, final_result_release_date, portfolio_score, tour, passing_type=None,
                 scan=None, participant=None):
        self.result = result
        self.participant = participant
        self.result_release_date = result_release_date
        self.final_result_release_date = get_final_result_release_date(final_result_release_date)
        # self.final_result_release_date = final_result_release_date
        self.portfolio_score = portfolio_score
        if portfolio_score is None:
            self.portfolio_score = 0
        self.score = self.get_final_score()
        self.tour = tour
        self.form = self.get_form()
        self.scan = self.get_scan()
        self.passing_type = self.get_passing_type()
        self.final_apply_form = self.get_final_form()
        # print('scan: ', self.scan, 'tour_order: ', self.tour.tour_order, 'participant: ', self.participant)
