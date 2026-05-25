from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from filters.admin_filter import AdminFilter

from database.db import (
    get_total_users,
    get_total_downloads,
    get_all_users,
    give_premium
)
import psutil

router = Router()

router.message.filter(
    AdminFilter()
)

@router.message(Command("stats"))
async def stats(message: Message):

    users = get_total_users()

    downloads = get_total_downloads()

    await message.answer(
        f"📊 BOT STATS\n\n"
        f"👥 Users: {users}\n"
        f"🎵 Downloads: {downloads}"
    )


@router.message(Command("broadcast"))
async def broadcast(
    message: Message
):

    text = message.text.replace(
        "/broadcast",
        ""
    ).strip()

    if not text:

        await message.answer(
            "❌ Text missing"
        )

        return

    users = get_all_users()

    success = 0
    failed = 0

    for user_id in users:

        try:

            await message.bot.send_message(
                user_id,
                text
            )

            success += 1

        except:

            failed += 1

    await message.answer(
        f"✅ Broadcast completed\n\n"
        f"✔ Success: {success}\n"
        f"❌ Failed: {failed}"
    )




@router.message(Command("ping"))
async def ping(message: Message):

    await message.answer(
        "🏓 Bot is alive"
    )

@router.message(Command("system"))
async def system_info(message: Message):

    cpu = psutil.cpu_percent()

    ram = psutil.virtual_memory().percent

    await message.answer(
        f"🖥 SYSTEM INFO\n\n"
        f"CPU: {cpu}%\n"
        f"RAM: {ram}%"
    )



@router.message(Command("givepremium"))
async def givepremium(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    parts = message.text.split()

    if len(parts) < 2:
        await message.answer(
            "Usage:\n/givepremium USER_ID"
        )
        return

    user_id = int(parts[1])

    give_premium(user_id)

    await message.answer(
        "✅ Premium added"
    )