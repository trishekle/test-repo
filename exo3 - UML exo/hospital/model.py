from datetime import datetime
from enum import Enum
from itertools import count


class ProblemStatus(Enum):
    PENDING = "pending"
    IN_REVIEW = "in_review"
    RESOLVED = "resolved"


# Allowed status transitions: current status -> statuses it may move to
_TRANSITIONS = {
    ProblemStatus.PENDING: {ProblemStatus.IN_REVIEW},
    ProblemStatus.IN_REVIEW: {ProblemStatus.RESOLVED},
    ProblemStatus.RESOLVED: set(),
}


class HealthProblem:
    _ids = count(1)

    def __init__(self, patient, description):
        self.id = next(HealthProblem._ids)
        self.patient = patient
        self.description = description
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.status = ProblemStatus.PENDING
        self.consultations = []   # 0..* Consultation

    def change_status(self, new_status):
        if new_status not in _TRANSITIONS[self.status]:
            raise ValueError(
                f"Illegal transition {self.status.name} -> {new_status.name}"
            )
        self.status = new_status
        self.updated_at = datetime.now()

    def __repr__(self):
        return f"HealthProblem(id={self.id}, status={self.status.name})"


class Consultation:
    """Association class between HealthProblem and Doctor."""

    def __init__(self, problem, doctor, notes=""):
        self.problem = problem
        self.doctor = doctor
        self.date = datetime.now()
        self.notes = notes
        self.prescription = None  # 0..1 Prescription
        # keep both sides of the association in sync
        problem.consultations.append(self)
        doctor.consultations.append(self)

    def __repr__(self):
        return f"Consultation(problem={self.problem.id}, doctor={self.doctor.name!r})"


class Prescription:
    _ids = count(1)

    def __init__(self, consultation, content, price):
        self.id = next(Prescription._ids)
        self.consultation = consultation
        self.content = content
        self.price = price
        self.issued_at = datetime.now()
        self.payment = None       # 0..1 Payment, set later
        consultation.prescription = self

    @property
    def patient(self):
        return self.consultation.problem.patient

    def __repr__(self):
        return f"Prescription(id={self.id}, price={self.price})"


if __name__ == "__main__":
    # Tiny stand-ins so this file can be tested without users.py
    class FakePatient:
        name = "Alice"

    class FakeDoctor:
        name = "Bob"
        consultations = []

    p = HealthProblem(FakePatient(), "headache")
    assert p.status is ProblemStatus.PENDING

    # Illegal jump is refused
    try:
        p.change_status(ProblemStatus.RESOLVED)
    except ValueError as e:
        print("OK:", e)

    p.change_status(ProblemStatus.IN_REVIEW)

    d = FakeDoctor()
    c = Consultation(p, d)
    assert c in p.consultations and c in d.consultations

    rx = Prescription(c, "rest + water", 30.0)
    assert c.prescription is rx
    assert rx.patient.name == "Alice"

    p.change_status(ProblemStatus.RESOLVED)
    try:
        p.change_status(ProblemStatus.PENDING)
    except ValueError as e:
        print("OK:", e)

    print(p, c, rx)