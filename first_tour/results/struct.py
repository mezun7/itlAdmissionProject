import datetime

from first_tour.forms import UserAppealForm
from first_tour.models import ExamResult, Tour, UserAppeal, TourParticipantScan


class ResultParticipant:
    result: list[ExamResult] = None
    passing_type: str = None
    result_release_date: datetime.datetime = None
    final_result_release_date: datetime.datetime = None
    scan: str = None
    score: int = None
    portfolio_score: int = 0
    tour: Tour = None
    form: UserAppealForm = None
    apeal_application: bool = False

    def get_form(self):
        participant = self.result[0].participant

        try:
            UserAppeal.objects.get(participant=participant, tour=self.tour)
            self.apeal_application = True
            return None
        except UserAppeal.DoesNotExist:
            if self.tour.appeal_application_end_date < datetime.datetime.now():
                return None
            return UserAppealForm(initial={
                'tour': self.tour,
                'participant': self.result[0].participant
            })

    def get_final_score(self):
        score = self.portfolio_score
        for subject in self.result:

            score += subject.score
            if subject.appeal_score is not None:
                score += subject.appeal_score

        return score

    def get_scan(self):
        try:
            return TourParticipantScan.objects.get(tour=self.tour,
                                                   participant=self.result[0].participant).scan_file_name
        except:
            return None

    def __init__(self, result, result_release_date, final_result_release_date, portfolio_score, tour, passing_type=None,
                 scan=None):
        self.result = result
        self.passing_type = passing_type
        self.result_release_date = result_release_date
        self.final_result_release_date = final_result_release_date

        self.portfolio_score = portfolio_score
        if portfolio_score is None:
            self.portfolio_score = 0
        self.score = self.get_final_score()
        self.tour = tour
        self.form = self.get_form()
        self.scan = self.get_scan()
