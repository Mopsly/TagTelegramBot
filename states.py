from aiogram.dispatcher.filters.state import State, StatesGroup


class AliasDlg(StatesGroup):
    none = State()
    alias = State()
