import logging

from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types

import database
import repository
from states import AliasDlg
from database import engine
import models
import os


API_TOKEN = "1692622341:AAFmylHjOSKsSsjzcw8vWmQD_48l2sVya7Q"
print(API_TOKEN)
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
models.Base.metadata.create_all(engine)


@dp.message_handler(commands=["cancel"], state="*")
async def cancel(message: types.Message, state: FSMContext):
    repository.update_user(message.from_user.id,
                           message.from_user.username,
                           False, database.session)
    await state.finish()
    await message.answer("Изменение списка псевдонимов отменено")


@dp.message_handler(commands=["setup"])
async def set_aliases(message: types.Message):
    user = repository.get_user(message.from_user.id, database.session)
    if not user:
        user = repository.new_user(message.from_user.id, message.from_user.username, database.session)
    alias_list = user.aliases
    list = []
    for alias in alias_list:
        if message.chat.id != alias.chat_id:
            continue
        list.append(alias.name)
    repository.update_user(user.tg_id, user.tag, True, database.session)
    if not alias_list:
        await message.answer("Ваш список псевдонимов пуст. Отправьте список псевдонимов через запятую")
    else:
        await message.answer(f"Ваш список псевдонимов: {list}. Отправьте новый список псевдонимов через запятую")
    await AliasDlg.alias.set()


@dp.message_handler(state=AliasDlg.alias)
async def receive_alias_list(message: types.Message, state: FSMContext):
    if message.is_command():
        return
    repository.update_user(message.from_user.id,
                           message.from_user.username,
                           False, database.session)
    msg = message.text.replace(" ", "").casefold()
    alias_list = msg.split(",")
    await message.answer(f"Ваш новый список псевдонимов: {alias_list}")
    repository.update_aliases(message.from_user.id, message.chat.id, alias_list, database.session)
    await state.finish()


@dp.message_handler()
async def tag_user(message: types.Message):
    aliases = repository.get_chat_aliases(message.chat.id, database.session)
    users = set()
    msg = " "
    for alias in aliases:
        if alias.name in message.text.casefold():
            users.add(alias.owner_id)
    for user in users:
        tag = repository.get_user(user, database.session).tag
        msg = msg + " @" + tag
    if msg != " ":
        await message.answer(msg)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)