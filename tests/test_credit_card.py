import pytest
from datetime import date
from app.models.credit_card import CreditCardModel


def test_exp_date_valid():
    # Data válida e maior que a data atual
    exp_date = date.today().replace(year=date.today().year + 1)
    cc = CreditCardModel(exp_date=exp_date)
    assert cc.is_exp_date_valid()


def test_exp_date_invalid():
    # Data inválida
    exp_date = "2022-13-01"  # Mês inválido
    cc = CreditCardModel(exp_date=exp_date)
    assert not cc.is_exp_date_valid()

    # Data menor que a data atual
    exp_date = date.today().replace(year=date.today().year - 1)
    cc = CreditCardModel(exp_date=exp_date)
    assert not cc.is_exp_date_valid()


def test_holder_valid():
    # Holder com mais de 2 caracteres
    holder = "John Doe"
    cc = CreditCardModel(holder=holder)
    assert cc.is_holder_valid()


def test_holder_invalid():
    # Holder vazio
    holder = ""
    cc = CreditCardModel(holder=holder)
    assert not cc.is_holder_valid()

    # Holder com menos de 2 caracteres
    holder = "A"
    cc = CreditCardModel(holder=holder)
    assert not cc.is_holder_valid()


def test_number_valid():
    # Número de cartão válido
    number = "4539578763621486"  # Visa card válido
    cc = CreditCardModel(number=number)
    assert cc.is_number_valid()


def test_number_invalid():
    # Número de cartão inválido
    number = "1111111111111111"
    cc = CreditCardModel(number=number)
    assert not cc.is_number_valid()


def test_cvv_valid():
    # CVV com 3 caracteres
    cvv = "123"
    cc = CreditCardModel(cvv=cvv)
    assert cc.is_cvv_valid()

    # CVV com 4 caracteres
    cvv = "1234"
    cc = CreditCardModel(cvv=cvv)
    assert cc.is_cvv_valid()


def test_cvv_invalid():
    # CVV com menos de 3 caracteres
    cvv = "12"
    cc = CreditCardModel(cvv=cvv)
    assert not cc.is_cvv_valid()

    # CVV com mais de 4 caracteres
    cvv = "12345"
    cc = CreditCardModel(cvv=cvv)
    assert not cc.is_cvv_valid()


@pytest.mark.parametrize(
    "exp_date, holder, number, cvv, is_valid",
    [
        # Caso válido
        (date.today().replace(year=date.today().year + 1), "John Doe", "4539578763621486", "123", True),
        # Caso inválido: Data inválida
        ("2022-13-01", "John Doe", "4539578763621486", "123", False),
        # Caso inválido: Holder inválido
        (date.today().replace(year=date.today().year + 1), "", "4539578763621486", "123", False),
        # Caso inválido: Número de cartão inválido
        (date.today().replace(year=date.today().year + 1), "John Doe", "1111111111111111", "123", False),
        # Caso inválido: CVV inválido
        (date.today().replace(year=date.today().year + 1), "John Doe", "4539578763621486", "12345", False),
    ]
)
def test_credit_card_validation(exp_date, holder, number, cvv, is_valid):
    cc = CreditCardModel(exp_date=exp_date, holder=holder, number=number, cvv=cvv)
    assert cc.is_valid() == is_valid
