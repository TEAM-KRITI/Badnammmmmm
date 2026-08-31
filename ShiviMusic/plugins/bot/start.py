# ===========================================================
# ©️ 2025-26 All Rights Reserved by Team Rocky (Im-Notcoder) 🚀
# 
# This source code is under MIT License 📜
# ❌ Unauthorized forking, importing, or using this code
#    without giving proper credit will result in legal action ⚠️
# 
# 📩 DM for permission : @MrRockytg
# ===========================================================

import time
import random
import asyncio
import os
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
import config
from ShiviMusic import app
from ShiviMusic.misc import _boot_
from ShiviMusic.plugins.sudo.sudoers import sudoers_list
from ShiviMusic.utils.database import get_served_chats, get_served_users, get_sudoers
from ShiviMusic.utils import bot_sys_stats
from ShiviMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from ShiviMusic.utils.decorators.language import LanguageStart
from ShiviMusic.utils.formatters import get_readable_time
from ShiviMusic.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string


NEXI_VID = [
    "https://files.catbox.moe/38tth5.jpg",
    "https://files.catbox.moe/ggfe0n.jpg",
    "https://files.catbox.moe/bv1u4q.jpg",
    "https://files.catbox.moe/dsmljb.jpg",
    "https://files.catbox.moe/l7gc2l.jpg",
    "https://files.catbox.moe/g2bmrf.jpg",
    "https://files.catbox.moe/9a8x0f.jpg",
    "https://files.catbox.moe/u451su.jpg",
    "https://files.catbox.moe/rf4toh.jpg",
    "https://files.catbox.moe/6tt01m.jpg",
    "https://files.catbox.moe/5es8qq.jpg",
    "https://files.catbox.moe/ydqnmt.jpg",
    "https://files.catbox.moe/7jds0u.jpg",
    "https://files.catbox.moe/hwydcv.jpg",
    "https://files.catbox.moe/y4m0yk.jpg",
]


# =======================================================
# ShiviMusic Join Request Premium Welcome
# =======================================================
JOIN_REQUEST_IMAGE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "assets",
    "shiviwel2.png",
)


def join_request_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("↗ ᴍᴏʀᴇ ɪɴғᴏ", callback_data="shivi_more_info")],
        [
            InlineKeyboardButton("↗ ᴜᴘᴅᴀᴛᴇ", url=config.SUPPORT_CHANNEL),
            InlineKeyboardButton("↗ sᴜᴘᴘᴏʀᴛ", url=config.SUPPORT_CHAT),
        ],
    ])


def join_request_text(user_name, chat_title):
    return (
        f"Welcome, — {user_name} !! 🇨🇦\n\n"
        f"Your request to join *{chat_title}* has been received.\n\n"
        "While you wait, explore — ᴄʜᴇᴇᴋᴜ 🍁.\n\n"
        "• High Quality Music\n"
        "• Fast & Smooth Playback\n"
        "• Stable Experience\n\n"
        "Use /start to begin."
    )


@app.on_chat_join_request()
async def shivi_join_request(client, join_request):
    """Send the premium welcome panel when a user requests to join."""
    user = join_request.from_user
    chat = join_request.chat
    chat_title = chat.title or config.BOT_NAME or "ShiviMusic"

    try:
        caption = join_request_text(user.first_name, chat_title)
        await client.send_photo(
            chat_id=user.id,
            photo=JOIN_REQUEST_IMAGE if os.path.exists(JOIN_REQUEST_IMAGE) else config.START_IMG_URL,
            caption=caption,
            parse_mode="markdown",
            reply_markup=join_request_keyboard(),
        )
        try:
            if await is_on_off(2):
                await client.send_message(
                    chat_id=config.LOGGER_ID,
                    text=(
                        f"✦ <b>JOIN REQUEST</b>\n\n"
                        f"✦ User: {user.mention}\n"
                        f"✦ ID: <code>{user.id}</code>\n"
                        f"✦ Chat: <b>{chat_title}</b>"
                    ),
                )
        except Exception as log_ex:
            print(f"Join request log error: {log_ex}")
    except Exception as ex:
        # Do not crash the music bot if Telegram rejects the private message.
        print(f"Join request welcome error for {user.id}: {ex}")


@app.on_callback_query(filters.regex(r"^shivi_more_info$"))
async def shivi_more_info(client, callback_query):
    await callback_query.answer()
    text = (
        "╭─━━━━━━━━━━━━━━─╮\n"
        "       🎧 ᴍᴏʀᴇ ɪɴғᴏ\n"
        "╰─━━━━━━━━━━━━━━─╯\n\n"
        "🎵 <b>ShiviMusic</b>\n\n"
        "• High Quality Music\n"
        "• Fast & Smooth Playback\n"
        "• Stable Experience\n"
        "• Premium Music Features\n\n"
        "✨ Enjoy your music with ShiviMusic!"
    )
    await callback_query.message.reply_text(
        text,
        parse_mode="html",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 ᴏᴡɴᴇʀ", url=f"https://t.me/{config.OWNER_USERNAME.lstrip('@')}"),
             InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url=config.SUPPORT_CHAT)],
            [InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇ", url=config.SUPPORT_CHANNEL)],
        ]),
    )


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]

        if name[0:3] == "del":
            await del_plist_msg(client=client, message=message, _=_)
        
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            return await message.reply_photo(
                random.choice(NEXI_VID),
                 has_spoiler=True,
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )

        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"✦ {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n<b>✦ ᴜsᴇʀ ɪᴅ ➠</b> <code>{message.from_user.id}</code>\n<b>✦ ᴜsᴇʀɴᴀᴍᴇ ➠</b> @{message.from_user.username}",
                )
            return

        if name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                        InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                 has_spoiler=True,
                caption=searched_text,
                reply_markup=key,
            )
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
    else:
        out = private_panel(_)
        await message.reply_photo(
            random.choice(NEXI_VID),
             has_spoiler=True,
            caption=_["start_2"].format(message.from_user.mention, app.mention),
            reply_markup=InlineKeyboardMarkup(out),
        )
        if await is_on_off(2):
            return await app.send_message(
                chat_id=config.LOGGER_ID,
                text=f"✦ {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n<b>✦ ᴜsᴇʀ ɪᴅ ➠</b> <code>{message.from_user.id}</code>\n<b>✦ ᴜsᴇʀɴᴀᴍᴇ ➠</b> @{message.from_user.username}",
            )          


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        random.choice(NEXI_VID),
         has_spoiler=True,
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                await message.reply_photo(
                    random.choice(NEXI_VID),
                     has_spoiler=True,
                    caption=_["start_3"].format(
                        message.from_user.mention,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)

# ===========================================================
# ©️ 2025-26 All Rights Reserved by Team Rocky (Im-Notcoder) 😎
# 
# 🧑‍💻 Developer : t.me/MrRockytg
# 🔗 Source link : t.me/Rockyxsupport
# 📢 Telegram channel : t.me/Rockyxupdate
# ===========================================================
