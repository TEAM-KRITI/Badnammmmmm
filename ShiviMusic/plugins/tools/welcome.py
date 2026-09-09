# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots
# =======================================================

import os
import asyncio
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
        {
            "$set": {
                "welcome": True
            }
        },
        upsert=True,
    )


async def disable_welcome(chat_id: int):

    await welcomedb.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "welcome": False
            }
        },
        upsert=True,
    )


# =======================================================
# TEMP STORAGE
# =======================================================

class temp:
    MELCOW = {}


# =======================================================
# CIRCLE PROFILE PHOTO
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

    draw = ImageDraw.Draw(mask)

    draw.ellipse(
        (
            0,
            0,
            size[0],
            size[1],
        ),
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
        size=(720, 720),
        brightness_factor=brightness_factor,
    )

    background.paste(
        pfp,
        (520, 420),
        pfp,
    )

    draw = ImageDraw.Draw(
        background
    )

    font_path = (
        "ShiviMusic/assets/font2.ttf"
    )

    try:

        font_id = ImageFont.truetype(
            font_path,
            100,
        )

        font_username = ImageFont.truetype(
            font_path,
            100,
        )

    except Exception as e:

        LOGGER.warning(
            f"Font loading failed: {e}"
        )

        font_id = ImageFont.load_default()
        font_username = ImageFont.load_default()

    username_text = (
        f"@{uname}"
        if uname
        else "ɴᴏᴛ sᴇᴛ"
    )

    draw.text(
        (1920, 1340),
        str(user_id),
        font=font_id,
        fill="#ffffff",
    )

    draw.text(
        (1920, 1480),
        username_text,
        font=font_username,
        fill="#ffffff",
    )

    output_path = (
        f"downloads/welcome_{user_id}.png"
    )

    background.save(
        output_path
    )

    return output_path


# =======================================================
# /WELCOME COMMAND
# =======================================================

@app.on_message(
    filters.command("welcome") & filters.group
)
async def welcome_cmd(_, message: Message):

    if not message.from_user:
        return

    chat = message.chat
    chat_id = chat.id

    # ---------------------------------------------------
    # ADMIN CHECK
    # ---------------------------------------------------

    try:

        member = await app.get_chat_member(
            chat_id,
            message.from_user.id,
        )

    except Exception as e:

        LOGGER.error(
            f"Admin check error: {e}"
        )

        return await message.reply_text(
            "⚠️ ᴜsᴇʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ɴᴏᴛ ғᴏᴜɴᴅ."
        )

    if member.status not in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):

        return await message.reply_text(
            "» ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ʜᴀɴᴅʟᴇ "
            "ᴡᴇʟᴄᴏᴍᴇ sʏsᴛᴇᴍ"
        )

    # ---------------------------------------------------
    # STATUS
    # ---------------------------------------------------

    state = await get_welcome(
        chat_id
    )

    status = (
        "ᴇɴᴀʙʟᴇᴅ"
        if state
        else "ᴅɪsᴀʙʟᴇᴅ"
    )

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ ᴇɴᴀʙʟᴇ",
                    callback_data=(
                        f"wlc_on_{chat_id}"
                    ),
                ),
                InlineKeyboardButton(
                    "❌ ᴅɪsᴀʙʟᴇ",
                    callback_data=(
                        f"wlc_off_{chat_id}"
                    ),
                ),
            ]
        ]
    )

    await message.reply_text(
        f"» ᴄᴜʀʀᴇɴᴛʟʏ ᴡᴇʟᴄᴏᴍᴇ sᴛᴀᴛᴜs : "
        f"**{status}**\n\n"
        f"» ɢʀᴏᴜᴘ : **{chat.title}**",
        reply_markup=buttons,
    )


# =======================================================
# WELCOME TOGGLE CALLBACK
# =======================================================

@app.on_callback_query(
    filters.regex(
        r"^wlc_(on|off)_"
    )
)
async def welcome_toggle(_, query):

    try:

        data = query.data.split("_")

        action = data[1]
        chat_id = int(data[2])

    except Exception:

        return await query.answer(
            "ɪɴᴠᴀʟɪᴅ ʀᴇǫᴜᴇsᴛ!",
            show_alert=True,
        )

    # ---------------------------------------------------
    # ADMIN CHECK
    # ---------------------------------------------------

    try:

        member = await app.get_chat_member(
            chat_id,
            query.from_user.id,
        )

    except Exception:

        return await query.answer(
            "ᴜɴᴀʙʟᴇ ᴛᴏ ᴄʜᴇᴄᴋ ᴀᴅᴍɪɴ sᴛᴀᴛᴜs!",
            show_alert=True,
        )

    if member.status not in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):

        return await query.answer(
            "ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ʙᴀʙʏ 🥺",
            show_alert=True,
        )

    # ---------------------------------------------------
    # ENABLE / DISABLE
    # ---------------------------------------------------

    if action == "on":

        await enable_welcome(
            chat_id
        )

        new_status = "ᴇɴᴀʙʟᴇᴅ"

    else:

        await disable_welcome(
            chat_id
        )

        new_status = "ᴅɪsᴀʙʟᴇᴅ"

    try:

        chat = await app.get_chat(
            chat_id
        )

        title = (
            chat.title
            or "ɢʀᴏᴜᴘ"
        )

    except Exception:

        title = "ɢʀᴏᴜᴘ"

    await query.message.edit_text(
        f"» ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇ "
        f"**{new_status}**\n\n"
        f"» ɢʀᴏᴜᴘ : **{title}**\n"
        f"» ʙʏ : {query.from_user.mention}"
    )

    await query.answer(
        f"ᴡᴇʟᴄᴏᴍᴇ {new_status}!"
    )


# =======================================================
# NEW MEMBER WELCOME
# =======================================================

@app.on_chat_member_updated(
    filters.group,
    group=-3,
)
async def greet_new_member(
    _,
    member: ChatMemberUpdated,
):

    chat_id = member.chat.id

    # ---------------------------------------------------
    # CHECK WELCOME ENABLED
    # ---------------------------------------------------

    is_enabled = await get_welcome(
        chat_id
    )

    if not is_enabled:
        return

    # ---------------------------------------------------
    # CHECK NEW MEMBER
    # ---------------------------------------------------

    if not member.new_chat_member:
        return

    user = member.new_chat_member.user

    if not user:
        return

    # ---------------------------------------------------
    # STATUS CHECK
    # ---------------------------------------------------

    old_status = (
        member.old_chat_member.status
        if member.old_chat_member
        else None
    )

    new_status = (
        member.new_chat_member.status
    )

    old_statuses = (
        None,
        enums.ChatMemberStatus.LEFT,
        enums.ChatMemberStatus.BANNED,
    )

    new_statuses = (
        enums.ChatMemberStatus.MEMBER,
        enums.ChatMemberStatus.RESTRICTED,
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    )

    if old_status not in old_statuses:
        return

    if new_status not in new_statuses:
        return

    # ---------------------------------------------------
    # DOWNLOAD PROFILE PHOTO
    # ---------------------------------------------------

    pic = (
        "ShiviMusic/assets/upic.png"
    )

    try:

        if (
            user.photo
            and user.photo.big_file_id
        ):

            downloaded = (
                await app.download_media(
                    user.photo.big_file_id,
                    file_name=(
                        f"downloads/pp{user.id}.png"
                    ),
                )
            )

            if downloaded:
                pic = downloaded

    except Exception as e:

        LOGGER.warning(
            f"Profile photo error: {e}"
        )

    # ---------------------------------------------------
    # DELETE PREVIOUS WELCOME
    # ---------------------------------------------------

    old = temp.MELCOW.get(
        f"welcome-{chat_id}"
    )

    if old:

        try:
            await old.delete()

        except Exception:
            pass

    # ---------------------------------------------------
    # GROUP INFORMATION
    # ---------------------------------------------------

    try:

        chat = await app.get_chat(
            chat_id
        )

        chat_title = (
            chat.title
            or "ɢʀᴏᴜᴘ"
        )

        members_count = (
            chat.members_count
            if chat.members_count is not None
            else "ɴ/ᴀ"
        )

    except Exception as e:

        LOGGER.warning(
            f"Group information error: {e}"
        )

        chat_title = "ɢʀᴏᴜᴘ"
        members_count = "ɴ/ᴀ"

    # ---------------------------------------------------
    # CREATE WELCOME IMAGE
    # ---------------------------------------------------

    try:

        welcomeimg = welcomepic(
            pic=pic,
            user=(
                user.first_name
                or "ᴜsᴇʀ"
            ),
            chatname=chat_title,
            user_id=user.id,
            uname=user.username,
        )

    except Exception as e:

        LOGGER.error(
            f"Welcome image error: {e}"
        )

        welcomeimg = pic

    # ---------------------------------------------------
    # USERNAME
    # ---------------------------------------------------

    username = (
        f"@{user.username}"
        if user.username
        else "ɴᴏᴛ sᴇᴛ"
    )

    # ---------------------------------------------------
    # NAME
    # ---------------------------------------------------

    name = (
        user.mention
        if user.first_name
        else "ᴜsᴇʀ"
    )

    # ===================================================
    # FINAL WELCOME CAPTION
    # ===================================================

    caption = f"""
<blockquote>
🌿💗 ‼️ ʀᴀᴅʜᴇ ᴋʀɪsʜɴᴀ ‼️ 💗🌿
</blockquote>

🎊 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ! 🎊

<blockquote expandable>
✦ ɴᴀᴍᴇ      → {name}
✦ ᴜsᴇʀɴᴀᴍᴇ  → {username}
✦ ᴜsᴇʀ ɪᴅ   → <code>{user.id}</code>
✦ ᴍᴇᴍʙᴇʀs   → <code>{members_count}</code>
</blockquote>

<blockquote>
🌸 sᴛᴀʏ ʜᴀᴘᴘʏ &amp; ᴇɴᴊᴏʏ ʏᴏᴜʀ ᴛɪᴍᴇ ʜᴇʀᴇ! 🌸
</blockquote>
"""

    # ===================================================
    # USER PROFILE URL
    # ===================================================

    profile_url = (
        f"tg://user?id={user.id}"
    )

    # ===================================================
    # BOT USERNAME
    # ===================================================

    try:

        me = await app.get_me()

        bot_username = me.username

    except Exception as e:

        LOGGER.warning(
            f"Bot username error: {e}"
        )

        bot_username = None

    # ===================================================
    # ADD ME URL
    # ===================================================

    if bot_username:

        add_me_url = (
            f"https://t.me/{bot_username}"
            f"?startgroup=true"
        )

    else:

        add_me_url = "https://t.me/"

    # ===================================================
    # BUTTONS
    # ===================================================

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "👤 ᴠɪᴇᴡ ᴘʀᴏғɪʟᴇ",
                    url=profile_url,
                )
            ],
            [
                InlineKeyboardButton(
                    "➕ ᴀᴅᴅ ᴍᴇ",
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
            chat_id=chat_id,
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
    # AUTO DELETE AFTER 200 SECONDS
    # ===================================================

    async def delete_welcome():

        await asyncio.sleep(200)

        try:

            await msg.delete()

        except Exception:
            pass

        temp.MELCOW.pop(
            f"welcome-{chat_id}",
            None,
        )

        # ------------------------------------------------
        # Delete generated image
        # ------------------------------------------------

        try:

            if (
                welcomeimg
                and welcomeimg.startswith(
                    "downloads/"
                )
                and os.path.exists(
                    welcomeimg
                )
            ):

                os.remove(
                    welcomeimg
                )

        except Exception:
            pass

    asyncio.create_task(
        delete_welcome()
    )

    temp.MELCOW[
        f"welcome-{chat_id}"
    ] = msg


# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots
# =======================================================
