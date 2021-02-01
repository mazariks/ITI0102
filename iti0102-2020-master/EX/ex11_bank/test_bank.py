"""Tests for Bank."""

import pytest
import bank
import datetime
import random
from string import digits

person1 = bank.Person("Mikk", "Kirg", 21)
person2 = bank.Person("Kim", "Truu", 14)
person3 = bank.Person("Andrei", "Grigorjev", 10)
bank1 = bank.Bank("Swedbank")
bank2 = bank.Bank("SEB")
bank3 = bank.Bank("LHV")


def test_error_person():
    """Test for person with illegal age."""
    with pytest.raises(bank.PersonError):
        bank.Person("Viga", "Error", -19213)


def test_full_name():
    """Test for a person's full name."""
    assert person1.full_name == "Mikk Kirg"
    assert person2.full_name == "Kim Truu"


def test_get_age():
    """Test for getting a person's age."""
    assert person1.age == 21
    assert person2.age == 14
    assert person3.age == 10


def test_set_age():
    """Test for setting a person's age."""
    with pytest.raises(bank.PersonError):
        person3.age = -10
    with pytest.raises(bank.PersonError):
        person1.age = 0
    person3.age = 100
    assert person3.age == 100


def test_person_repr():
    """Test for person's string representation."""
    assert person1.__repr__() == person1.full_name
    assert person2.__repr__() == "Kim Truu"


def test_add_customer():
    """Test for adding customer to a bank."""
    bank1.add_customer(person1)
    assert person1 in bank1.customers
    assert person1.bank_account is not None
    assert person2 not in bank1.customers and person3 not in bank1.customers
    bank3.add_customer(person2)
    assert person2 in bank3.customers
    assert bank3.add_customer(person2) is False


def test_remove_customer():
    """Test for removing customer from a bank."""
    bank1.add_customer(person1)
    bank3.add_customer(person2)
    bank1.remove_customer(person1)
    assert person1 not in bank1.customers
    assert person1.bank_account is None
    assert bank3.remove_customer(person3) is False


def test_bank_repr():
    """Test for a bank name representation."""
    assert bank1.__repr__() == bank1.name
    assert bank2.__repr__() != "Nordea"
    assert bank3.__repr__() == "LHV"


def test_transaction_repr():
    """Test for a transaction's representation."""
    bank1.add_customer(person1)
    bank1.add_customer(person2)
    bank3.add_customer(person3)
    transaction1 = bank.Transaction(10, datetime.date.today(), person1.bank_account, person2.bank_account, False)
    assert transaction1.__repr__() == "(10 €) Mikk Kirg -> Kim Truu"
    transaction2 = bank.Transaction(100, datetime.date.today(), person3.bank_account, person3.bank_account, True)
    assert transaction2.__repr__() == "(100 €) ATM"


def test_get_balance():
    """Test for getting a balance of account."""
    account1 = bank.Account(0, person1, bank1)
    account2 = bank.Account(1000, person3, bank2)
    assert account2.balance == 1000
    assert account1.balance != account2.balance
    assert account1.balance in range(10)


def test_deposit():
    """Test for depositing some money to account."""
    account1 = bank.Account(0, person1, bank1)
    account2 = bank.Account(1000, person3, bank2)
    account1.deposit(100)
    assert account1.balance == 100
    with pytest.raises(bank.TransactionError):
        account2.deposit(-10)


def test_withdraw():
    """Test for withdrawing some money from account."""
    account1 = bank.Account(0, person1, bank1)
    account2 = bank.Account(1000, person3, bank2)
    with pytest.raises(bank.TransactionError):
        account1.withdraw(10)
    account2.withdraw(25)
    assert account2.balance == 975


def test_transfer():
    """Test for transferring some money from one account to another."""
    account1 = bank.Account(0, person1, bank1)
    account2 = bank.Account(1000, person3, bank2)
    with pytest.raises(bank.TransactionError):
        account1.transfer(25, account2)
    with pytest.raises(bank.TransactionError):
        account2.transfer(100, account2)
    account2.transfer(599, account1)
    assert account2.balance == 396  # 401 - 5 since different banks.
    assert account1.balance == 599


def test_account_statement():
    """Test for making a transactions' view of account between 2 dates."""
    account1 = bank.Account(0, person1, bank1)
    account2 = bank.Account(1000, person3, bank2)
    assert account1.account_statement(datetime.date.today() - datetime.timedelta(days=10), datetime.date.today()) == []
    account1.deposit(157)
    account2.withdraw(212)
    account1.transfer(57, account2)
    assert len(account1.account_statement(datetime.date.today() - datetime.timedelta(days=10), datetime.date.today())) \
           == 2


def test_debit_turnover():
    """Test for a review of a total incomes of account between 2 dates."""
    account1 = bank.Account(0, person1, bank1)
    account2 = bank.Account(1000, person3, bank2)
    assert account1.get_debit_turnover(datetime.date.today() - datetime.timedelta(days=10), datetime.date.today()) == 0
    account1.deposit(25)
    account2.transfer(987, account1)
    assert account1.get_debit_turnover(datetime.date.today() - datetime.timedelta(days=10), datetime.date.today()) \
           == 1012


def test_credit_turnover():
    """Test for a review of costs of account between 2 dates."""
    account1 = bank.Account(0, person1, bank1)
    account2 = bank.Account(1000, person3, bank2)
    account2.withdraw(412)
    account2.transfer(214, account1)
    assert account1.get_credit_turnover(datetime.date.today() - datetime.timedelta(days=10), datetime.date.today()) == 0
    assert account2.get_credit_turnover(datetime.date.today() - datetime.timedelta(days=10), datetime.date.today()) \
           == -626


def test_get_net_turnover():
    """Test of overall statistics of account between 2 dates."""
    account1 = bank.Account(0, person1, bank1)
    account2 = bank.Account(1000, person3, bank2)
    assert account1.get_net_turnover(datetime.date.today() - datetime.timedelta(days=10), datetime.date.today()) \
           == account2.get_net_turnover(datetime.date.today() - datetime.timedelta(days=10), datetime.date.today()) == 0
    account2.withdraw(412)
    account2.transfer(214, account1)
    account1.deposit(25)
    account1.transfer(57, account2)
    assert account1.get_net_turnover(datetime.date.today() - datetime.timedelta(days=10), datetime.date.today()) == 182
    assert account2.get_net_turnover(datetime.date.today() - datetime.timedelta(days=10), datetime.date.today()) == -569


def test_account_repr():
    """Test for account's representation."""
    account1 = bank.Account(0, person1, bank1)
    account2 = bank.Account(1000, person3, bank2)
    random_number = "EE" + ''.join(random.choices(digits, k=18))
    assert account1.__repr__() != random_number
    assert account2.__repr__() != random_number
    assert account2.__repr__() != account1.__repr__()
    assert "EE" in account1.__repr__() and "EE" in account2.__repr__()
    assert len(account1.__repr__()) == 20 and len(account2.__repr__()) == 20
