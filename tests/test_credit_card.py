from app.models.credit_card import CreditCard


def test_credit_card_model():
    cc = CreditCard(
        id=1,
        exp_date="2023-10-01",
        holder="John Doe",
        number="1234123412341234",
        cvv="123",
    )
    assert cc.id == 1
    assert cc.exp_date == "2023-10-01"
    assert cc.holder == "John Doe"
    assert cc.number == "1234123412341234"
    assert cc.cvv == "123"
