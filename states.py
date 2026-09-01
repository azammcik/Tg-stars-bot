from aiogram.fsm.state import State, StatesGroup


class CardPayment(StatesGroup):
    waiting_receipt = State()
