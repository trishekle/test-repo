from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum


class PaymentStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    FORWARDED = "forwarded"


class Payment(ABC):
    """Strategy interface: each payment type implements process() its own way."""

    def __init__(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.amount = amount
        self.date = datetime.now()
        self.status = PaymentStatus.PENDING

    @abstractmethod
    def process(self):
        """Carry out the payment according to the payment type."""

    def confirm_receipt(self):
        """PENDING -> PAID. Called by process() or by the organizer (checks)."""
        if self.status is not PaymentStatus.PENDING:
            raise ValueError(f"Cannot confirm a payment that is {self.status.name}")
        self.status = PaymentStatus.PAID

    def forward(self):
        """PAID -> FORWARDED. Can only happen once, and only after payment."""
        if self.status is not PaymentStatus.PAID:
            raise ValueError(f"Cannot forward a payment that is {self.status.name}")
        self.status = PaymentStatus.FORWARDED

    def __repr__(self):
        return f"{type(self).__name__}(amount={self.amount}, status={self.status.name})"


class Cash(Payment):
    def process(self):
        self.confirm_receipt()          # cash is received immediately


class CreditCard(Payment):
    def __init__(self, amount, card_number):
        super().__init__(amount)
        self.card_number = card_number

    def process(self):
        digits = self.card_number.replace(" ", "")
        if not (digits.isdigit() and len(digits) == 16):
            raise ValueError("Invalid card number")
        self.confirm_receipt()          # charged immediately if the card is valid


class Check(Payment):
    def __init__(self, amount, check_number):
        super().__init__(amount)
        self.check_number = check_number

    def process(self):
        pass                            # stays PENDING until the organizer confirms receipt


if __name__ == "__main__":
    try:
        Payment(10)
    except TypeError:
        print("OK: Payment is abstract")

    cash = Cash(30)
    cash.process()
    assert cash.status is PaymentStatus.PAID

    chk = Check(30, "A123")
    chk.process()
    assert chk.status is PaymentStatus.PENDING
    chk.confirm_receipt()
    assert chk.status is PaymentStatus.PAID

    cash.forward()
    try:
        cash.forward()
    except ValueError:
        print("OK: cannot forward twice")

    try:
        CreditCard(30, "1234").process()
    except ValueError:
        print("OK: invalid card refused")