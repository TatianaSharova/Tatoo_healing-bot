from aiogram import F, Router, types
from filters.chat_types import IsAdmin
from aiogram import F, Router, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.methods import forward_message
from typing import List
from aiogram.methods.send_media_group import SendMediaGroup
from aiogram.types import Message, InputMediaPhoto, InputMediaVideo, ContentType as CT

from dotenv import load_dotenv
import os
load_dotenv()
ADMIN_2 = int(os.getenv('ADMIN_2'))


admin_router = Router()
admin_router.message.filter(IsAdmin())

# FSM
class Post(StatesGroup):

    post = State()

    ready = None


@admin_router.message(
        StateFilter("*"), Command("cancel"))
@admin_router.message(
    StateFilter("*"), or_f(F.text.casefold() == "отмена",
                           F.text.casefold() == "cancel"))
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    if Post.ready:
        Post.ready = None
    await state.clear()
    await message.answer(
        'Действия отменены.')


@admin_router.message(Command('admin'))
@admin_router.message(F.text.lower() == 'admin')
async def get_help(message: types.Message) -> types.Message:
    await message.answer(
        'админка',
        parse_mode=ParseMode.HTML,
        )


@admin_router.message(
        StateFilter(None), F.text.strip().lower() == 'post')
@admin_router.message(StateFilter(None), Command('post'))
async def post(message: types.Message,  state: FSMContext) -> types.Message:
    await message.answer(
        'Пришлите пост, который хотите разослать подписчикам.',
        parse_mode=ParseMode.HTML,
        )
    await state.set_state(Post.post)


# пример отправки тех же данных в виде медиагруппы
@admin_router.message(Post.post,
                      F.media_group_id != None,
                      F.content_type.in_([
                          CT.PHOTO, CT.VIDEO
                      ]))
async def handle_albums(message: Message, album: list[Message]):
    media_group = []
    first = True
    for msg in album:
        if msg.photo:
            file_id = msg.photo[-1].file_id
            if first:
                media_group.append(InputMediaPhoto(
                    media=file_id,
                    caption=message.caption))
                first = False
            else:
                media_group.append(InputMediaPhoto(
                        media=file_id))
        if msg.video:
            file_id = msg.video.file_id
            if first:
                media_group.append(InputMediaVideo(
                    media=file_id, caption=message.caption))
            else:
                media_group.append(InputMediaVideo(media=file_id))

    await message.answer_media_group(media_group)


@admin_router.message(Post.post,
                      F.content_type.in_({'text', 'photo', 'video'}))
async def send_post(message: types.Message, state: FSMContext):
    await message.send_copy(chat_id=ADMIN_2)
