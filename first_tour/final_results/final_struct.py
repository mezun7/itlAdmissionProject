from admission.models import Participant
from first_tour.models import ExamResult, ExamSubject, Tour, LiterGrade


class FinalResult:
    participant: Participant = None
    results: [ExamResult] = None
    tour: Tour = None
    overall = 0
    recommended = True
    zachet = True
    exam_subjects: [ExamSubject] = None
    liter: LiterGrade = None

    def calc_result(self):
        types = {
            'Z': self.zachet,
            'R': self.recommended
        }
        ex_results = ExamResult.objects.filter(participant=self.participant,
                                               exam_subject__tour=self.tour)
        # print(len(ex_results), self.participant)

        subjects = list(self.exam_subjects.values_list('subject__name', flat=True))
        # print(len(subjects))
        results = [None] * len(subjects)

        for ex in ex_results:
            # ex: ExamResult
            type_of_scoring = ex.exam_subject.type_of_scoring
            pos: int = subjects.index(ex.exam_subject.subject.name)
            results[pos] = ex
            if type_of_scoring in ['Z', 'R']:
                types[type_of_scoring] = not ex.score < 1
            else:
                self.overall += ex.score
        # print(results)
        if self.participant.extra_score:
            self.overall += self.participant.extra_score
        return results

    def __init__(self, participant, tour, exam_subjects, liter_grade):
        self.participant = participant
        self.tour = tour
        self.exam_subjects = exam_subjects
        self.liter = liter_grade
        self.results = self.calc_result()

    def __lt__(self, other):
        if self.overall == other.overall:
            if self.recommended == other.recommended:
                if self.zachet == other.zachet:
                    # print(self.participant.id < other.participant.id)
                    return self.participant.id > other.participant.id
                else:
                    return self.zachet < other.zachet
            else:
                return self.recommended < other.recommended
        return self.overall < other.overall
