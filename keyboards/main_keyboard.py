from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def media_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📥 Видео",
                    callback_data="video"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🎵 MP3",
                    callback_data="mp3"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🎧 Full Song",
                    callback_data="full_song"
                ),
            ]
        ]
    )

    return keyboard