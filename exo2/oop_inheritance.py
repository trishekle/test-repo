## Inheritance

### Problem 1
# Create a class `Vehicle` that has a method `drive` that returns the string "Driving a vehicle". Create two subclasses, `Car` and `Bicycle`, that override this method to return "Driving a car" and "Riding a bicycle", respectively.

class Vehicle:
    def drive(self):
        return "Driving a vehicle"

class Car(Vehicle):
    def drive(self):
        return "Driving a car"

class Bicycle(Vehicle):
    def drive(self):
        return "Riding a bicycle"

if __name__ == "__main__":
    vehicles = [Vehicle(), Car(), Bicycle()]
    for v in vehicles:
        print(v.drive())

    assert Vehicle().drive() == "Driving a vehicle"
    assert Car().drive() == "Driving a car"
    assert Bicycle().drive() == "Riding a bicycle"


### Problem 2
#Create a class `Person` with attributes: `name`, `age`, `address` and method: `introduce`.

# Create a subclass `Student` of the class `Person` that has an attribute: `field_of_study` and a personalized method: `introduce`.

# Create another subclass `Employee` of the class `Person` that has an attribute: `company` and a personalized method: `introduce`.

class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def introduce(self):
        return f"Hello, my name is {self.name}, I am {self.age} years old and I live at {self.address}."

class Student(Person):
    def __init__(self, name, age, address, field_of_study):
        super().__init__(name, age, address)
        self.field_of_study = field_of_study

    def introduce(self):
        return f"Hello, my name is {self.name}, I am {self.age} years old, I live at {self.address} and I study {self.field_of_study}."

class Employee(Person):
    def __init__(self, name, age, address, company):
        super().__init__(name, age, address)
        self.company = company

    def introduce(self):
        return f"Hello, my name is {self.name}, I am {self.age} years old, I live at {self.address} and I work at {self.company}."

### Problem 3
# Define two classes, `BankAccount` and `SavingsAccount`:

#- `BankAccount` has attributes `account_number` and `balance`, and methods `deposit` and `withdraw`
#- `SavingsAccount` inherits from `BankAccount` and adds `interest_rate` attribute and `add_interest` method
#- Add a `check_balance` method to `SavingsAccount`
#- Add a `transfer` method to `BankAccount` that transfers money to a destination account (return `False` if insufficient balance, `True` otherwise)

class BankAccount:
    def __init__(self, account_number, balance):
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def transfer(self, destination_account, amount):
        if self.withdraw(amount):
            destination_account.deposit(amount)
            return True
        return False

class SavingsAccount(BankAccount):
    def __init__(self, account_number, balance, interest_rate):
        super().__init__(account_number, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        self.balance += self.balance * self.interest_rate

    def check_balance(self):
        return self.balance
