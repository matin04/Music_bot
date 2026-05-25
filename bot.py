from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram import F
import asyncio
from dotenv import load_dotenv
import os
from aiogram.types import Message, FSInputFile
from services.downloader import download_instagram_video
from services.music_recognizer import recognize_music
from services.song_downloader import download_full_song
from constants import *
from keyboards.main_keyboard import media_keyboard
from aiogram.types import CallbackQuery
from utils.cache_utils import (
    get_cached_song_path,
    save_to_cache
)
from database.db import (
    create_tables,
    add_user,
    add_download,
    get_total_users,
    get_total_downloads,
    save_user_link,
    get_user_link,
    delete_user_link,
    is_premium
)
from database.queries import (
    create_tables,
    add_user,
    add_download,
    get_total_users,
    get_total_downloads
)

from utils.logger import logger
import traceback
from utils.cleaner import (
    delete_file,
    delete_old_files
)
from urllib.parse import urlparse
from services.audio_extractor import (
    extract_audio
)
from utils.rate_limiter import RateLimiter
from utils.task_queue import TaskQueue
from aiogram.fsm.context import FSMContext
from states.user_states import UserStates
from middlewares.logging_middleware import LoggingMiddleware
from middlewares.rate_limit_middleware import (
    RateLimitMiddleware
)
from handlers.admin import router as admin_router
from utils.redis_cache import (
    cache_song,
    get_cached_song
)
from utils.redis_rate_limit import (
    RedisRateLimiter
)
from handlers.ai import router as ai_router
from middlewares.limits import (
    can_download,
    add_download
)
from handlers.premium import (
    router as premium_router
)



rate_limiter = RedisRateLimiter()


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError(
        "BOT_TOKEN not found in .env"
    )

logger.info("Creating database tables...")
# create_tables()
bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(admin_router)
dp.update.middleware(
    LoggingMiddleware()
)
dp.update.middleware(
    RateLimitMiddleware()
)
dp.include_router(ai_router)
dp.include_router(
    premium_router
)
rate_limiter = RateLimiter(cooldown_seconds=4)
task_queue = TaskQueue()
# add_user
# user_links = {}


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(
    UserStates.waiting_link
    )
    await add_user(message.from_user.id)
    await message.answer(START_TEXT)

@dp.message(UserStates.waiting_link, F.text)
async def get_link(message: Message, state: FSMContext):

    if not rate_limiter.is_allowed(message.from_user.id):
        await message.answer("⏳ Лутфан каме интизор шавед...")
        return

    text = (message.text or "").strip()
    if not text:
        return

    logger.info(
        f"User {message.from_user.id} sent: {text}"
    )
# get_total_users
    
    allowed_domains = [
        "instagram.com",
        "tiktok.com",
        "youtube.com",
        "youtu.be",
        "facebook.com"
    ]

    parsed = urlparse(text)

    domain = parsed.netloc.lower()

    is_link = any(
        allowed in domain
        for allowed in allowed_domains
    )

    # SEARCH MODE 🔍
    if not is_link and len(text) < 3:

        if len(text) < 2:
            await message.answer(INVALID_LINK)
            return

        await message.answer(
            SEARCHING_SONG
        )
# user_links
# user_id
# cached_song
# text
# url
        try:

            full_song_path = await asyncio.to_thread(
                download_full_song,
                text
            )

            song = FSInputFile(full_song_path)

            await message.answer_audio(
                song,
                caption=f"🎵 Search Result\n\n{text}"
            )

            await asyncio.sleep(2)
            delete_file(full_song_path)

        except Exception as e:
            logger.error(
                traceback.format_exc()
            )
            await message.answer(
                f"❌ Хато:\n{e}"
            )

        return

    # LINK MODE 🔥
    await state.update_data(
        url=text
    )

    await message.answer(
        "🎬 Чӣ мехоҳӣ?",
        reply_markup=media_keyboard()
    )

    await state.set_state(
        UserStates.choosing_media
    )

# create_tables()

async def main():
    delete_old_files("downloads")
    delete_old_files("cache", hours=72)

    logger.info("Old files cleaned")
    logger.info("Starting bot polling...")

    asyncio.create_task(task_queue.worker())

    await dp.start_polling(bot)
    await create_tables()

@dp.callback_query(F.data == "video")
async def send_video(callback: CallbackQuery, state: FSMContext):

    if not rate_limiter.is_allowed(callback.from_user.id):
        await callback.answer("⏳ Оҳиста!", show_alert=True)
        return
    
    await state.set_state(
        UserStates.processing
    )
    
    
    data = await state.get_data()

    url = data.get("url")

    if not is_premium(callback.from_user.id):

        if not can_download(
            callback.from_user.id
        ):
    
            await callback.message.answer(
                "🚫 Free лимит тамом шуд.\n"
                "⭐ Premium гир!"
            )
    
            return
    
        add_download(
            callback.from_user.id
        )

    if not url:
        await callback.message.answer("❌ Ссылка ёфт нашуд.")
        return
    
    
    await callback.message.answer(DOWNLOADING_VIDEO)
    
    try:
        video_path = await asyncio.to_thread(
            download_instagram_video,
            url
        )

        video = FSInputFile(video_path)

        async def process_video():
            await callback.message.answer_video(video)

        task_queue.add_task(process_video())

        await asyncio.sleep(2)

        delete_file(video_path)
# keyboard:
        logger.info(
            f"Video downloaded by user {callback.from_user.id}"
        )

    except Exception as e:
        logger.error(
            traceback.format_exc()
        )
        await callback.message.answer(f"❌ Хато:\n{e}")

    await callback.answer()

    
@dp.callback_query(F.data == "mp3")
async def send_mp3(callback: CallbackQuery, state: FSMContext):

    if not rate_limiter.is_allowed(callback.from_user.id):
        await callback.answer("⏳ Оҳиста!", show_alert=True)
        return
    
    await state.set_state(
        UserStates.processing
    )

    await callback.answer()

    url = get_user_link(
        callback.from_user.id
    )
# cached_song 

    if not is_premium(callback.from_user.id):

        if not can_download(
            callback.from_user.id
        ):

            await callback.message.answer(
                "🚫 Free лимит тамом шуд.\n"
                "⭐ Premium гир!"
            )

            return

        add_download(
            callback.from_user.id
        )

    if not url:
        await callback.message.answer("❌ Ссылка ёфт нашуд.")
        return
    
    try:
        status = await callback.message.answer(DOWNLOADING_VIDEO)
        
        await bot.send_chat_action(
            callback.message.chat.id,
            "upload_video"
        )

        video_path = await asyncio.to_thread(
            download_instagram_video,
            url
        )
        await status.edit_text(EXTRACTING_AUDIO)

        await bot.send_chat_action(
            callback.message.chat.id,
            "upload_audio"
        )

        audio_path = await asyncio.to_thread(
            extract_audio,
            video_path
        )

        if not os.path.exists(audio_path):
            raise Exception(
                "Audio extraction failed"
        )

        audio = FSInputFile(audio_path)

        if not os.path.exists(audio_path):
            raise Exception("Audio extraction failed")

        async def process_mp3():
            await callback.message.answer_audio(audio)
        
        task_queue.add_task(process_mp3())

        await asyncio.sleep(2)

        delete_file(video_path)
        delete_file(audio_path)

        delete_user_link(
            callback.from_user.id
        )

        logger.info(
            f"MP3 sent to user {callback.from_user.id}"
        )

    except Exception as e:
        logger.exception(
            "MP3 sending error"
        )
        await callback.message.answer(f"❌ Хато:\n{e}")

    


def normalize_query(query):
    return (
        query
        .lower()
        .strip()
    )

@dp.callback_query(F.data == "full_song")
async def send_full_song(callback: CallbackQuery, state: FSMContext):

    if not rate_limiter.is_allowed(callback.from_user.id):
        await callback.answer("⏳ Оҳиста!", show_alert=True)
        return
    
    await state.set_state(
        UserStates.processing
    )

    url = get_user_link(
        callback.from_user.id
    )

    if not is_premium(callback.from_user.id):

        if not can_download(
            callback.from_user.id
        ):
    
            await callback.message.answer(
                "🚫 Free лимит тамом шуд.\n"
                "⭐ Premium гир!"
            )
    
            return
    
        add_download(
            callback.from_user.id
        )

    # logger.info(
    #     f"Song sent successfully: {query}"
    # )
# await callback.message.answer_audio(audio)

    if not url:
        await callback.message.answer("❌ Ссылка ёфт нашуд.")
        return
    
    video_path = None
    audio_path = None
    full_song_path = None

    try:
        
        await bot.send_chat_action(
            callback.message.chat.id,
            "upload_video"
        )

        status = await callback.message.answer(DOWNLOADING_VIDEO)

        await bot.send_chat_action(
            callback.message.chat.id,
            "upload_audio"
        )

        video_path = await asyncio.to_thread(
            download_instagram_video,
            url
        )

        await status.edit_text(EXTRACTING_AUDIO)

        audio_path = await asyncio.to_thread(
            extract_audio,
            video_path
        )

        await status.edit_text(RECOGNIZING_MUSIC)

        music_info = await asyncio.to_thread(
            recognize_music,
            audio_path
        )

        if music_info.get("result"):

            title = music_info["result"].get(
                "title",
                "Unknown"
            )

            artist = music_info["result"].get(
                "artist",
                "Unknown"
            )

            spotify_link = None
            apple_music_link = None
            cover_image = None

            if music_info["result"].get("spotify"):
                spotify_link = music_info["result"]["spotify"]["external_urls"]["spotify"]
                images = music_info["result"]["spotify"]["album"]["images"]
                if images:
                    cover_image = images[0]["url"]

            if music_info["result"].get("apple_music"):
                apple_music_link = music_info["result"]["apple_music"]["url"]

            query = normalize_query(
                f"{title} {artist}"
            )
            logger.info(
                f"User {callback.from_user.id} downloaded: {query}"
            )

            add_download(
                callback.from_user.id,
                query
            )
# save_to_cache
            cached_song = get_cached_song(query)

            if cached_song:

                video_path = None
                audio_path = None
                full_song_path = None

                logger.info(
                    f"Cache hit: {query}"
                )
            
                await callback.message.answer(
                    "⚡ Суруд аз cache ёфт шуд!"
                )

                if cover_image:
                    await callback.message.answer_photo(
                        photo=cover_image,
                        caption=(
                            f"🖼 Album Cover\n\n"
                            f"🎵 {title}\n"
                            f"👤 {artist}"
                        )
                    )

                # if not os.path.exists(full_song_path):
                #     raise Exception(
                #         "Full song download failed"
                #     )

                full_song = FSInputFile(cached_song)

                await bot.send_chat_action(
                    callback.message.chat.id,
                    "upload_audio"
                )

                await callback.message.answer_audio(
                    full_song,
                    caption=(
                        f"🎵 {title}\n"
                        f"👤 {artist}\n\n"
                        f"🔥 Downloaded by Music Bot"
                    ),
                    title=title,
                    performer=artist,
                )

                await asyncio.sleep(2)

                # delete_file(cached_song)

                await callback.answer()

                delete_user_link(
                    callback.from_user.id
                )

                return

            text = (
                f"🎵 Суруд ёфт шуд!\n\n"
                f"📌 Ном: {title}\n"
                f"👤 Сароянда: {artist}\n"
            )
            if spotify_link:
                text += f"\n🎧 Spotify:\n{spotify_link}\n"

            if apple_music_link:
                text += f"\n🍎 Apple Music:\n{apple_music_link}\n"

            await callback.message.answer(text)

            await status.edit_text(
                DOWNLOADING_FULL_SONG
            )

            full_song_path = await asyncio.to_thread(
                download_full_song,
                query
            )

            cache_song(
                query,
                full_song_path
            )
# audio
            full_song = FSInputFile(full_song_path)

            await bot.send_chat_action(
                callback.message.chat.id,
                "upload_audio"
            )

            async def process_full_song():

                await callback.message.answer_audio(
                    full_song,
                    caption=(
                        f"🎵 {title}\n"
                        f"👤 {artist}\n\n"
                        f"🔥 Downloaded by Music Bot"
                    ),
                    title=title,
                    performer=artist
                )

            task_queue.add_task(process_full_song())

            delete_file(full_song_path)

            logger.info(
            f"Song sent successfully: {query}"
            )
            
        


        else:
            await callback.message.answer(
                MUSIC_NOT_FOUND
            )

        delete_file(video_path)
        delete_file(audio_path)

    except Exception as e:
        logger.exception(
            "Full song error"
        )
        await callback.message.answer(f"❌ Хато:\n{e}")

    finally:

        for f in [video_path, audio_path, full_song_path]:
            if f:
                delete_file(f)
        
        await state.clear()

        delete_user_link(
            callback.from_user.id
        )

    await callback.answer()
    
@dp.message(F.text == "/stats")
async def stats(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    users = await get_total_users()

    downloads = get_total_downloads()

    await message.answer(
        f"📊 Статистика\n\n"
        f"👥 Users: {users}\n"
        f"🎵 Downloads: {downloads}"
        f"💾 Cache Size: coming soon\n"
    )


if __name__ == "__main__":
    asyncio.run(main())