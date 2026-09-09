# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots
# =======================================================

import os
import asyncio
from datetime import datetime
from logging import getLogger

from motor.motor_asyncio import AsyncIOMotorClient
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

from pyrogram import filters, enums
from pyrogram.types import (
    ChatMemberUpdated,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
)

from ShiviMusic import app
from config import MONGO_DB_URI


LOGGER = getLogger(__name__)


# =======================================================
# 📋 LOGGER GROUP ID
# =======================================================
# अपना Telegram Logger Group ID यहाँ डालें

LOG_GROUP_ID = -1003989793155


# =======================================================
# DATABASE
# =======================================================

mongo = AsyncIOMotorClient(MONGO_DB_URI)

db = mongo["Wel_DB"]
welcomedb = db["welcome_toggle_system"]


# =======================================================
# DOWNLOAD FOLDER
# =======================================================

os.makedirs("downloads", exist_ok=True)


# =======================================================
# WELCOME DATABASE
# =======================================================

async def get_welcome(chat_id: int):

    data = await welcomedb.find_one(
        {"chat_id": chat_id}
    )

    if not data:
        return True

    return data.get("welcome", True)


async def enable_welcome(chat_id: int):

    await welcomedb.update_one(
        {"chat_id": chat_id},
        {"$set": {"welcome": True}},
        upsert=True,
    )


async def disable_welcome(chat_id: int):

    await welcomedb.update_one(
        {"chat_id": chat_id},
        {"$set": {"welcome": False}},
        upsert=True,
    )


# =======================================================
# TEMP
# =======================================================

class temp:
    MELCOW = {}


# =======================================================
# CIRCLE PHOTO
# =======================================================

def circle(
    pfp,
    size=(720, 720),
    brightness_factor=1.4,
):

    pfp = pfp.resize(size).convert("RGBA")

    pfp = ImageEnhance.Brightness(
        pfp
    ).enhance(brightness_factor)

    mask = Image.new(
        "L",
        size,
        0,
    )

    ImageDraw.Draw(mask).ellipse(
        (0, 0, size[0], size[1]),
        fill=255,
    )

    pfp.putalpha(mask)

    return pfp


# =======================================================
# WELCOME IMAGE
# =======================================================

def welcomepic(
    pic,
    user,
    chatname,
    user_id,
    uname,
    brightness_factor=1.3,
):

    background = Image.open(
        "ShiviMusic/assets/wel2.png"
    ).convert("RGBA")

    pfp = Image.open(
        pic
    ).convert("RGBA")

    pfp = circle(
        pfp,
        (720, 720),
        brightness_factor,
    )

    background.paste(
        pfp,
        (520, 420),
        pfp,
    )

    draw = ImageDraw.Draw(background)

    try:

        font = ImageFont.truetype(
            "ShiviMusic/assets/font2.ttf",
            100,
        )

    except Exception:

        font = ImageFont.load_default()

    username_text = (
        f"@{uname}"
        if uname
        else "𝐍σт 𝐒єт"
    )

    draw.text(
        (1920, 1340),
        str(user_id),
        font=font,
        fill="#ffffff",
    )

    draw.text(
        (1920, 1480),
        username_text,
        font=font,
        fill="#ffffff",
    )

    output = f"downloads/welcome_{user_id}.png"

    background.save(output)

    return output


# =======================================================
# /WELCOME
# =======================================================

@app.on_message(
    filters.command("welcome") & filters.group
)
async def welcome_cmd(_, message: Message):

    if not message.from_user:
        return

    chat_id = message.chat.id

    try:

        member = await app.get_chat_member(
            chat_id,
            message.from_user.id,
        )

    except Exception:

        return await message.reply_text(
            "⚠️ 𝐔ѕєя 𝐈ηƒσямαтιση 𝐍σт 𝐅συη∂."
        )

    if member.status not in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):

        return await message.reply_text(
            "» 𝐎ηℓу 𝐀∂мιηѕ 𝐂αη 𝐇αη∂ℓє "
            "𝐖єℓ¢σмє 𝐒уѕтєм."
        )

    state = await get_welcome(chat_id)

    status = (
        "𝐄ηαвℓє∂"
        if state
        else "𝐃ιѕαвℓє∂"
    )

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ 𝐄ηαвℓє",
                    callback_data=f"wlc_on_{chat_id}",
                ),
                InlineKeyboardButton(
                    "❌ 𝐃ιѕαвℓє",
                    callback_data=f"wlc_off_{chat_id}",
                ),
            ]
        ]
    )

    await message.reply_text(
        f"» 𝐂υяяєηтℓу 𝐖єℓ¢σмє 𝐒тαтυѕ : "
        f"**{status}**\n\n"
        f"» 𝐆яσυρ : **{message.chat.title}**",
        reply_markup=buttons,
    )


# =======================================================
# TOGGLE CALLBACK
# =======================================================

@app.on_callback_query(
    filters.regex(r"^wlc_(on|off)_")
)
async def welcome_toggle(_, query):

    try:

        parts = query.data.split("_")
        action = parts[1]
        chat_id = int(parts[2])

    except Exception:

        return await query.answer(
            "𝐈ηναℓι∂ 𝐑єqυєѕт!",
            show_alert=True,
        )

    try:

        member = await app.get_chat_member(
            chat_id,
            query.from_user.id,
        )

    except Exception:

        return await query.answer(
            "𝐔ηαвℓє тσ 𝐂нє¢к 𝐀∂мιη!",
            show_alert=True,
        )

    if member.status not in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):

        return await query.answer(
            "𝐘συ 𝐀яє ησт αη 𝐀∂мιη!",
            show_alert=True,
        )

    if action == "on":

        await enable_welcome(chat_id)
        new_status = "𝐄ηαвℓє∂"

    else:

        await disable_welcome(chat_id)
        new_status = "𝐃ιѕαвℓє∂"

    try:

        chat = await app.get_chat(chat_id)
        title = chat.title or "𝐆яσυρ"

    except Exception:

        title = "𝐆яσυρ"

    await query.message.edit_text(
        f"» 𝐖єℓ¢σмє 𝐌єѕѕαgє "
        f"**{new_status}**\n\n"
        f"» 𝐆яσυρ : **{title}**\n"
        f"» 𝐁у : {query.from_user.mention}"
    )

    await query.answer(
        f"𝐖єℓ¢σмє {new_status}!"
    )


# =======================================================
# 👤 JOIN + LEFT + WELCOME
# =======================================================

@app.on_chat_member_updated(
    filters.group,
    group=-3,
)
async def member_update(_, member: ChatMemberUpdated):

    if not member.new_chat_member:
        return

    user = member.new_chat_member.user

    if not user:
        return

    old_status = (
        member.old_chat_member.status
        if member.old_chat_member
        else None
    )

    new_status = member.new_chat_member.status

    join_status = (
        enums.ChatMemberStatus.MEMBER,
        enums.ChatMemberStatus.RESTRICTED,
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    )

    left_status = (
        enums.ChatMemberStatus.LEFT,
        enums.ChatMemberStatus.BANNED,
    )

    is_join = (
        old_status in (
            None,
            enums.ChatMemberStatus.LEFT,
            enums.ChatMemberStatus.BANNED,
        )
        and new_status in join_status
    )

    is_left = new_status in left_status

    if not is_join and not is_left:
        return

    chat = member.chat

    # ===================================================
    # USER DATA
    # ===================================================

    if user.last_name:

        name = (
            f"{user.first_name} "
            f"{user.last_name}"
        )

    else:

        name = user.first_name or "𝐍σт 𝐍αмє"

    username = (
        f"@{user.username}"
        if user.username
        else "𝐍σ 𝐔ѕєяηαмє"
    )

    public_profile = bool(
        user.username
    )

    group_link = bool(
        chat.username
    )

    now = datetime.now().strftime(
        "%d-%m-%Y • %I:%M %p"
    )

    # ===================================================
    # LOGGER CAPTION
    # ===================================================

    if is_join:

        log_caption = f"""
👤 𝐍єω 𝐌ємвєя 𝐉σιηє∂

👤 𝐍αмє: {name}
🔖 𝐔ѕєяηαмє: {username}
🆔 𝐔ѕєя 𝐈𝐃: {user.id}
⏰ 𝐉σιη 𝐓ιмє: {now}
👥 𝐆яσυρ: {chat.title}

🌐 𝐏υвℓι¢ 𝐏яσƒιℓє: {"𝐎ρєη 𝐏υвℓι¢ 𝐏яσƒιℓє" if public_profile else "𝐍σ 𝐏υвℓι¢ 𝐔ѕєяηαмє"}
👤 𝐏яινтє 𝐏яσƒιℓє: 𝐎ρєη 𝐏яινтє 𝐏яσƒιℓє
👥 𝐆яσυρ 𝐋ιηк: {"𝐎ρєη 𝐆яσυρ" if group_link else "𝐍σ 𝐏υвℓι¢ 𝐆яσυρ 𝐋ιηк"}
"""

    else:

        log_caption = f"""
👤 𝐌ємвєя 𝐋єƒт

👤 𝐍αмє: {name}
🔖 𝐔ѕєяηαмє: {username}
🆔 𝐔ѕєя 𝐈𝐃: {user.id}
⏰ 𝐋єƒт 𝐓ιмє: {now}
👥 𝐆яσυρ: {chat.title}

🌐 𝐏υвℓι¢ 𝐏яσƒιℓє: {"𝐎ρєη 𝐏υвℓι¢ 𝐏яσƒιℓє" if public_profile else "𝐍σ 𝐏υвℓι¢ 𝐔ѕєяηαмє"}
👤 𝐏яινтє 𝐏яσƒιℓє: 𝐎ρєη 𝐏яινтє 𝐏яσƒιℓє
👥 𝐆яσυρ 𝐋ιηк: {"𝐎ρєη 𝐆яσυρ" if group_link else "𝐍σ 𝐏υвℓι¢ 𝐆яσυρ 𝐋ιηк"}
"""

    # ===================================================
    # 📋 SEND TO TELEGRAM LOGGER
    # ===================================================

    try:

        await app.send_photo(
            chat_id=LOG_GROUP_ID,
            photo="ShiviMusic/assets/wel2.png",
            caption=log_caption,
        )

    except Exception as e:

        LOGGER.error(
            f"Telegram logger error: {e}"
        )

    # ===================================================
    # LEFT → STOP HERE
    # ===================================================

    if is_left:
        return

    # ===================================================
    # WELCOME CHECK
    # ===================================================

    if not await get_welcome(chat.id):
        return

    # ===================================================
    # PROFILE PHOTO
    # ===================================================

    pic = "ShiviMusic/assets/upic.png"

    try:

        if user.photo and user.photo.big_file_id:

            downloaded = await app.download_media(
                user.photo.big_file_id,
                file_name=f"downloads/pp_{user.id}.png",
            )

            if downloaded:
                pic = downloaded

    except Exception as e:

        LOGGER.warning(
            f"Profile photo error: {e}"
        )

    # ===================================================
    # DELETE OLD WELCOME
    # ===================================================

    old = temp.MELCOW.get(
        f"welcome-{chat.id}"
    )

    if old:

        try:
            await old.delete()

        except Exception:
            pass

    # ===================================================
    # CREATE WELCOME IMAGE
    # ===================================================

    try:

        welcomeimg = welcomepic(
            pic=pic,
            user=name,
            chatname=chat.title or "𝐆яσυρ",
            user_id=user.id,
            uname=user.username,
        )

    except Exception as e:

        LOGGER.error(
            f"Welcome image error: {e}"
        )

        welcomeimg = pic

    # ===================================================
    # WELCOME CAPTION
    # ===================================================

    welcome_username = (
        f"@{user.username}"
        if user.username
        else "𝐍σт 𝐒єт"
    )

    caption = f"""
<blockquote>
🌿💗 ‼️ 𝐑α∂нє 𝐊яιѕнηα ‼️ 💗🌿
</blockquote>

🎊 𝐖єℓ¢σмє тσ тнє 𝐆яσυρ! 🎊

<blockquote expandable>
✦ 𝐍αмє → {user.mention}
✦ 𝐔ѕєяηαмє → {welcome_username}
✦ 𝐔ѕєя 𝐈𝐃 → <code>{user.id}</code>
✦ 𝐌ємвєяѕ → <code>{chat.members_count or "𝐍/𝐀"}</code>
</blockquote>

<blockquote>
🌸 𝐒тαу 𝐇αρρу &amp; 𝐄ηנσу 𝐘συя 𝐓ιмє 𝐇єяє! 🌸
</blockquote>
"""

    # ===================================================
    # VIEW PROFILE
    # ===================================================

    profile_url = (
        f"https://t.me/{user.username}"
        if user.username
        else f"tg://user?id={user.id}"
    )

    # ===================================================
    # BOT USERNAME
    # ===================================================

    try:

        me = await app.get_me()
        bot_username = me.username

    except Exception:

        bot_username = None

    add_me_url = (
        f"https://t.me/{bot_username}?startgroup=true"
        if bot_username
        else "https://t.me/"
    )

    # ===================================================
    # BUTTONS
    # ===================================================

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "👤 𝐕ιєω 𝐏яσƒιℓє",
                    url=profile_url,
                )
            ],
            [
                InlineKeyboardButton(
                    "➕ 𝐀∂∂ 𝐌є",
                    url=add_me_url,
                )
            ],
        ]
    )

    # ===================================================
    # SEND WELCOME
    # ===================================================

    try:

        msg = await app.send_photo(
            chat_id=chat.id,
            photo=welcomeimg,
            caption=caption,
            parse_mode=enums.ParseMode.HTML,
            reply_markup=buttons,
        )

    except Exception as e:

        LOGGER.error(
            f"Welcome send error: {e}"
        )

        return

    # ===================================================
    # AUTO DELETE
    # ===================================================

    async def delete_welcome():

        await asyncio.sleep(200)

        try:
            await msg.delete()
        except Exception:
            pass

        temp.MELCOW.pop(
            f"welcome-{chat.id}",
            None,
        )

        try:

            if (
                welcomeimg
                and welcomeimg.startswith("downloads/")
                and os.path.exists(welcomeimg)
            ):

                os.remove(welcomeimg)

        except Exception:
            pass

        try:

            if (
                pic.startswith("downloads/")
                and os.path.exists(pic)
            ):

                os.remove(pic)

        except Exception:
            pass

    asyncio.create_task(
        delete_welcome()
    )

    temp.MELCOW[
        f"welcome-{chat.id}"
    ] = msg


# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots
# ====
