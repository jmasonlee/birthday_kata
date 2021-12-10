import datetime
from abc import abstractmethod, ABC
from collections import namedtuple
from unittest import TestCase

BirthdayMessage = namedtuple("BirthdayMessage", "subject message")
Employee = namedtuple("Employee", "name birthdate")


class GetEmployeeNamesAndBirthdates(ABC):
    @abstractmethod
    def do(self):
        pass


class SendEmail(ABC):
    @abstractmethod
    def do(self, messages):
        pass


class TestSendEmail(SendEmail):
    email_messages = []

    def do(self, messages):
        self.email_messages = messages


class TestGetEmployeeNameAndBirthdates(GetEmployeeNamesAndBirthdates):
    def __init__(self, employees):
        self.employees = employees

    def do(self):
        return self.employees


class DateCompare:
    def __init__(self, today_date):
        self._today_date = today_date

    def is_birthday_on_date(self, birthdate, date):
        return birthdate.day == date.day and birthdate.month == date.month


class BirthdayMessenger:
    def __init__(self, get_employee_names_and_birthdates, send_email, today_date):
        self.get_employee_names_and_birthdates = get_employee_names_and_birthdates
        self.send_email = send_email
        self.today_date = today_date

    def send_birthday_greeting(self):
        employees = self.get_employee_names_and_birthdates.do()

        messages = []
        for employee in employees:
            is_employee_birthday_today = employee.birthdate.day == self.today_date.day and employee.birthdate.month == self.today_date.month
            if is_employee_birthday_today:
                messages.append(BirthdayMessage("Happy birthday!", f"Happy birthday, dear {employee.name}!"))

        self.send_email.do(messages)


class Test(TestCase):

    def test_send_birthday_message_for_employees_with_birthday_today(self):
        today = datetime.datetime(2034, 2, 1).date()
        employee1 = Employee("John", today)
        get_employee_name_and_birthdate = TestGetEmployeeNameAndBirthdates([employee1])

        send_email = TestSendEmail()
        BirthdayMessenger(get_employee_name_and_birthdate, send_email, today).send_birthday_greeting()

        self.assertEqual([(BirthdayMessage("Happy birthday!", "Happy birthday, dear John!"))],
                         send_email.email_messages)

    def test_do_not_send_birthday_message_for_employees_with_birthday_not_today(self):
        employee1 = Employee("John", datetime.datetime(2010, 1, 1))
        get_employee_name_and_birthdate = TestGetEmployeeNameAndBirthdates([employee1])
        send_email = TestSendEmail()

        not_today = datetime.datetime(2019, 9, 4)
        BirthdayMessenger(get_employee_name_and_birthdate, send_email, not_today).send_birthday_greeting()

        self.assertEqual([], send_email.email_messages)

    def test_send_birthday_message_to_multiple_employees(self):
        today = datetime.datetime.today().date()
        employee1 = Employee("GeePaw", DateCompare(today)._today_date)
        employee2 = Employee("John", DateCompare(today)._today_date)
        get_employee_name_and_birthdate = TestGetEmployeeNameAndBirthdates([employee1, employee2])
        send_email = TestSendEmail()

        BirthdayMessenger(get_employee_name_and_birthdate, send_email, today).send_birthday_greeting()

        self.assertEqual([BirthdayMessage("Happy birthday!", "Happy birthday, dear GeePaw!"),
                          BirthdayMessage("Happy birthday!", "Happy birthday, dear John!")],
                         send_email.email_messages)

    def test_send_birthday_message_to_multiple_employees_more_than_5_years_old(self):
        birthday = datetime.date(2018, 3, 5)
        employee1 = Employee("GeePaw", birthday)
        employee2 = Employee("John", birthday)
        get_employee_name_and_birthdate = TestGetEmployeeNameAndBirthdates([employee1, employee2])
        send_email = TestSendEmail()

        BirthdayMessenger(get_employee_name_and_birthdate, send_email, datetime.date(2021, 3, 5)).send_birthday_greeting()

        self.assertEqual([BirthdayMessage("Happy birthday!", "Happy birthday, dear GeePaw!"),
                          BirthdayMessage("Happy birthday!", "Happy birthday, dear John!")],
                         send_email.email_messages)
