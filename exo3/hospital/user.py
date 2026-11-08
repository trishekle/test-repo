from abc import ABC, abstractmethod
from itertools import count
import hashlib

from models import HealthProblem, Consultation, Prescription, ProblemStatus


class User(ABC):
    _ids = count(1)  # shared counter: every user, whatever the subclass, gets a unique id

    def __init__(self, name, password):
        self.id = next(User._ids)
        self.name = name
        self._password_hash = self._hash(password)
        self.is_logged_in = False

    @staticmethod
    def _hash(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, password):
        if self._hash(password) == self._password_hash:
            self.is_logged_in = True
            return True
        return False

    def logout(self):
        self.is_logged_in = False

    @property
    @abstractmethod
    def role(self):
        """Each subclass returns its role name. This makes User abstract."""

    def __repr__(self):
        return f"{self.role.capitalize()}(id={self.id}, name={self.name!r})"


class Patient(User):
    def __init__(self, name, password, address):
        super().__init__(name, password)
        self.address = address
        self.problems = []        # 0..* HealthProblem
        self.prescriptions = []   # 0..* Prescription (history)

    @property
    def role(self):
        return "patient"

    def post_problem(self, description):
        problem = HealthProblem(self, description)
        self.problems.append(problem)
        return problem

    def pay(self, prescription, payment):
        if prescription.patient is not self:
            raise ValueError("This prescription belongs to another patient")
        if prescription.payment is not None:
            raise ValueError("This prescription is already paid")
        if payment.amount != prescription.price:
            raise ValueError("Payment amount does not match the prescription price")
        prescription.payment = payment
        payment.process()          # polymorphism: Cash, Check or CreditCard behaves differently
        return payment


class Doctor(User):
    def __init__(self, name, password, speciality):
        super().__init__(name, password)
        self.speciality = speciality
        self.consultations = []   # 0..* Consultation
        self.earnings = 0.0

    @property
    def role(self):
        return "doctor"

    def write_prescription(self, consultation, content, price):
        if consultation.doctor is not self:
            raise ValueError("This consultation belongs to another doctor")
        prescription = Prescription(consultation, content, price)
        consultation.problem.change_status(ProblemStatus.RESOLVED)
        return prescription


class Organizer(User):
    def __init__(self, name, password):
        super().__init__(name, password)
        self.members = []         # everyone this organizer has registered

    @property
    def role(self):
        return "organizer"

    def create_member(self, member_cls, name, password, *extra):
        """Issue an id and password for a new Patient or Doctor.
        extra = address for Patient, speciality for Doctor."""
        if member_cls not in (Patient, Doctor):
            raise ValueError("Organizer can only create a Patient or a Doctor")
        member = member_cls(name, password, *extra)
        self.members.append(member)
        return member

    def consult_doctor(self, problem, doctor):
        problem.change_status(ProblemStatus.IN_REVIEW)
        return Consultation(problem, doctor)

    def send_prescription(self, prescription, patient):
        if prescription.patient is not patient:
            raise ValueError("Prescription does not belong to this patient")
        patient.prescriptions.append(prescription)

    def confirm_receipt(self, payment):
        """For checks: the organizer confirms the money arrived."""
        payment.confirm_receipt()

    def forward_payment(self, payment, doctor):
        payment.forward()          # raises unless PAID, so it can only happen once
        doctor.earnings += payment.amount


if __name__ == "__main__":
    # 1. User is abstract
    try:
        User("x", "y")
    except TypeError:
        print("OK: User cannot be instantiated")

    # 2. Registration
    org = Organizer("Admin", "root")
    alice = org.create_member(Patient, "Alice", "pw1", "12 rue X")
    bob = org.create_member(Doctor, "Bob", "pw2", "cardiology")
    assert len(org.members) == 2
    assert alice.id != bob.id

    # 3. Login
    assert alice.login("pw1") is True
    assert alice.is_logged_in
    assert alice.login("wrong") is False
    alice.logout()
    assert not alice.is_logged_in

    # 4. Wrong member type is rejected
    try:
        org.create_member(Organizer, "Eve", "pw")
    except ValueError:
        print("OK: cannot create an Organizer this way")

    print(alice, bob, org)