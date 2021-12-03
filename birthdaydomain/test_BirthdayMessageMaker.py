import datetime
from abc import abstractmethod, ABC
from collections import namedtuple
from unittest import TestCase

TODAY = datetime.datetime.today().date()

BirthdayMessage = namedtuple("BirthdayMessage", "subject message")
Employee = namedtuple("Employee", "name birthdate")


class GetEmployeeNamesAndBirthdates(ABC):
    @abstractmethod
    def do(self):
        pass


class TestGetEmployeeNameAndBirthdates(GetEmployeeNamesAndBirthdates):
    def __init__(self, employees):
        self.employees = employees

    def do(self):
        return self.employees


class BirthdayMessenger:
    def __init__(self, get_employee_names_and_birthdates):
        self.get_employee_names_and_birthdates = get_employee_names_and_birthdates

    def send_birthday_greeting(self):
        employees = self.get_employee_names_and_birthdates.do()

        messages = BirthdayMessage("", "")
        for employee in employees:
            is_employee_birthday_today = employee.birthdate == TODAY
            if is_employee_birthday_today:
                return BirthdayMessage("Happy birthday!", f"Happy birthday, dear {employee.name}!")

        return messages


class Test(TestCase):

    def test_send_birthday_message_for_employees_with_birthday_today(self):
        employee1 = Employee("John", TODAY)
        get_employee_name_and_birthdate = TestGetEmployeeNameAndBirthdates([employee1])
        expectedOutput = BirthdayMessage("Happy birthday!", "Happy birthday, dear John!")
        self.assertEqual(expectedOutput, BirthdayMessenger(get_employee_name_and_birthdate).send_birthday_greeting())

    def test_do_not_send_birthday_message_for_employees_with_birthday_not_today(self):
        employee1 = Employee("John", datetime.datetime(2010, 1, 1))
        get_employee_name_and_birthdate = TestGetEmployeeNameAndBirthdates([employee1])
        self.assertEqual(BirthdayMessage("", ""),
                         BirthdayMessenger(get_employee_name_and_birthdate).send_birthday_greeting())

    def test_send_birthday_message_to_multiple_employees(self):
        employee1 = Employee("GeePaw", TODAY)
        employee2 = Employee("John", datetime.datetime.today())
        get_employee_name_and_birthdate = TestGetEmployeeNameAndBirthdates([employee1])
        self.assertEqual([BirthdayMessage("Happy birthday!", "Happy birthday, dear GeePaw!"),
                          BirthdayMessage("Happy birthday!", "Happy birthday, dear John!")],
                         BirthdayMessenger(get_employee_name_and_birthdate).send_birthday_greeting())
