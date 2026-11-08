from users import Organizer, Patient, Doctor
from models import ProblemStatus
from payments import Cash, Check, CreditCard, PaymentStatus


def run(payment_factory, label):
    print(f"\n--- Scenario: {label} ---")

    # SSD 1: registration
    org = Organizer("Admin", "root")
    alice = org.create_member(Patient, "Alice", "pw1", "12 rue X")
    bob = org.create_member(Doctor, "Bob", "pw2", "cardiology")

    # SSD 2: consultation flow
    assert alice.login("pw1")
    problem = alice.post_problem("Persistent headache")
    assert problem.status is ProblemStatus.PENDING

    consultation = org.consult_doctor(problem, bob)
    assert problem.status is ProblemStatus.IN_REVIEW

    prescription = bob.write_prescription(consultation, "Rest and hydration", 30.0)
    assert problem.status is ProblemStatus.RESOLVED

    org.send_prescription(prescription, alice)
    assert prescription in alice.prescriptions

    # SSD 3: payment flow
    payment = payment_factory(prescription.price)
    alice.pay(prescription, payment)
    if payment.status is PaymentStatus.PENDING:      # a check needs manual confirmation
        org.confirm_receipt(payment)
    assert payment.status is PaymentStatus.PAID

    org.forward_payment(payment, bob)
    assert payment.status is PaymentStatus.FORWARDED
    assert bob.earnings == 30.0

    # Forwarding twice must fail
    try:
        org.forward_payment(payment, bob)
    except ValueError:
        print("OK: double forward refused")

    print(problem, consultation, prescription, payment, sep="\n")


if __name__ == "__main__":
    run(lambda amount: Cash(amount), "cash")
    run(lambda amount: Check(amount, "A123"), "check")
    run(lambda amount: CreditCard(amount, "1234 5678 9012 3456"), "credit card")
    print("\nAll scenarios passed.")