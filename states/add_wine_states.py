from aiogram.dispatcher.filters.state import StatesGroup, State

class WineAdderState(StatesGroup):
    photo = State()
    wine = State()
    score = State()
    grape = State()
    sugar = State()
    color = State()
    country = State()
    producer = State()
    year = State()
    location = State()
    price = State()
    comment = State()


class WineSearchState(StatesGroup):
    search = State()
    options = State()
    serch_by_name = State()
    serch_by_color = State()
    serch_by_sugar = State()


class WineSearchStateAdmin(StatesGroup):
    search = State()
    options = State()
    serch_by_name = State()
    serch_by_color = State()
    serch_by_sugar = State()


class AddBarcode(StatesGroup):
    bc_photo = State()
    wine_photo = State()
    