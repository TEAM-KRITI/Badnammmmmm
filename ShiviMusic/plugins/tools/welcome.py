# ===========================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀
#
# This source code is under MIT License 📜
# ===========================================================

import os
import asyncio
from logging import getLogger

from motor.motor_asyncio import AsyncIOMotorClient
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

from pyrogram import filters, enums
from pyrogram.errors import (
    FloodWait,
    ChatSendPhotosForbidden,
    ChatWriteForbidden,
    MessageNotModified,
    MessageIdInvalid,
)

from pyrogram.types import (
    ChatMemberUpdated,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
)

from config import MONGO_DB_URI
from ShiviMusic import app


LOGGER = getLogger(__name__)


# ===========================================================
# MONGODB
# ===========================================================

mongo = AsyncIOMotorClient(MONGO_DB_URI)

db = mongo["Wel_DB"]
welcomedb = db["welcome_toggle_system"]


# ===========================================================
# WELCOME DATABASE
# ===========================================================

async def get_welcome(chat_id: int):

    data = await welcomedb.find_one(
        {"chat_id": chat_id}
    )

    if not data:
        return True

    return data.get(
        "welcome",
        True,
    )


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


# ===========================================================
# TEMP STORAGE
# ===========================================================

class temp:
    MELCOW = {}


# ===========================================================
# CREATE DOWNLOAD DIRECTORY
# ===========================================================

os.makedirs(
    "downloads",
    exist_ok=True,
)


# ===========================================================
# CIRCLE PROFILE PHOTO
# ===========================================================

def circle(
    pfp,
    size=(720, 720),
    brightness_factor=1.4,
):

    pfp = pfp.resize(
        size
    ).convert(
        "RGBA"
    )

    pfp = ImageEnhance.Brightness(
        pfp
    ).enhance(
        brightness_factor
    )

    mask = Image.new(
        "L",
        size,
        0,
    )

    draw = ImageDraw.Draw(
        mask
    )

    draw.ellipse(
        (
            0,
            0,
            size[0],
            size[1],
        ),
        fill=255,
    )

    pfp.putalpha(
        mask
    )

    return pfp


# ===========================================================
# WELCOME IMAGE
# ===========================================================

def welcomepic(
    pic,
    user,
    chatname,
    id,
    uname,
    brightness_factor=1.3,
):

    background = Image.open(
        "ShiviMusic/assets/wel2.png"
    ).convert(
        "RGBA"
    )

    pfp = Image.open(
        pic
    ).convert(
        "RGBA"
    )

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

    font_id = ImageFont.truetype(
        font_path,
        100,
    )

    font_username = ImageFont.truetype(
        font_path,
        100,
    )

    username_text = (
        f"@{uname}"
        if uname
        else "Not Set"
    )

    draw.text(
        (1920, 1340),
        str(id),
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
        f"downloads/welcome_{id}.png"
    )

    background.save(
        output_path
    )

    return output_path


# ===========================================================
# ADMIN CHECK
# ===========================================================

async def is_admin(
    chat_id: int,
    user_id: int,
):

    try:

        member = await app.get_chat_member(
            chat_id,
            user_id,
        )

        return member.status in (
            enums.ChatMemberStatus.ADMINISTRATOR,
            enums.ChatMemberStatus.OWNER,
        )

    except Exception:

        return False


# ===========================================================
# WELCOME COMMAND
# ===========================================================

@app.on_message(
    filters.command(
        "welcome"
    )
    & filters.group
)
async def welcome_cmd(
    _,
    message: Message,
):

    if not message.from_user:
        return

    chat = message.chat
    chat_id = chat.id

    if not await is_admin(
        chat_id,
        message.from_user.id,
    ):

        return await message.reply_text(
            "**» ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ʜᴀɴᴅʟᴇ "
            "ᴡᴇʟᴄᴏᴍᴇ ꜱʏꜱᴛᴇᴍ**"
        )

    state = await get_welcome(
        chat_id
    )

    status = (
        "ᴇɴᴀʙʟᴇᴅ"
        if state
        else "ᴅɪꜱᴀʙʟᴇᴅ"
    )

    btn = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "ᴇɴᴀʙʟᴇ",
                    callback_data=f"wlc_on_{chat_id}",
                ),
                InlineKeyboardButton(
                    "ᴅɪsᴀʙʟᴇ",
                    callback_data=f"wlc_off_{chat_id}",
                ),
            ]
        ]
    )

    await message.reply_text(
        f"» ᴄᴜʀʀᴇɴᴛʟʏ ᴡᴇʟᴄᴏᴍᴇ ꜱᴛᴀᴛᴜꜱ "
        f"**{status}** ɪɴ **{chat.title}**",
        reply_markup=btn,
    )


# ===========================================================
# WELCOME TOGGLE
# ===========================================================

@app.on_callback_query(
    filters.regex(
        r"^wlc_(on|off)_(-?\d+)$"
    )
)
async def welcome_toggle(
    _,
    query,
):

    try:

        data = query.data.split(
            "_"
        )

        action = data[1]
        chat_id = int(data[2])

    except Exception:

        return await query.answer(
            "ɪɴᴠᴀʟɪᴅ ʀᴇǫᴜᴇsᴛ.",
            show_alert=True,
        )

    if not await is_admin(
        chat_id,
        query.from_user.id,
    ):

        return await query.answer(
            "ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ʙᴀʙʏ 🥺",
            show_alert=True,
        )

    try:

        if action == "on":

            await enable_welcome(
                chat_id
            )

            new_status = "ᴇɴᴀʙʟᴇᴅ"

        else:

            await disable_welcome(
                chat_id
            )

            new_status = "ᴅɪꜱᴀʙʟᴇᴅ"

        chat = await app.get_chat(
            chat_id
        )

        text = (
            f"» ᴡᴇʟᴄᴏᴍᴇ ᴍᴇꜱꜱᴀɢᴇ "
            f"**{new_status}** "
            f"ɪɴ **{chat.title}**\n\n"
            f"ʙʏ :- {query.from_user.mention}"
        )

        try:

            await query.message.edit_text(
                text
            )

        except (
            MessageNotModified,
            MessageIdInvalid,
        ):

            pass

        await query.answer(
            "ᴜᴘᴅᴀᴛᴇᴅ ✅"
        )

    except Exception as e:

        LOGGER.exception(
            "Welcome toggle error: %s",
            e,
        )

        await query.answer(
            "ᴇʀʀᴏʀ ᴡʜɪʟᴇ ᴜᴘᴅᴀᴛɪɴɢ.",
            show_alert=True,
        )


# ===========================================================
# SEND TEXT WELCOME
# ===========================================================

async def send_text_welcome(
    chat_id,
    user,
    chat_title,
):

    username = (
        f"@{user.username}"
        if user.username
        else "Not Set"
    )

    text = f"""
**⏤͟͟͞͞★ ʜᴇʟʟᴏ ᴅᴇᴀʀ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ : {chat_title}**

<u>**❖ ᴜsᴇʀ sʜᴏʀᴛ ɪɴғᴏ**</u>

**➻ ɴᴀᴍᴇ »** {user.mention}
**➻ ᴄʜᴀᴛ_ɪᴅ »** `{user.id}`
**➻ ᴜ_ɴᴀᴍᴇ »** {username}

**➻ ᴛʜᴀɴᴋs ғᴏʀ ᴊᴏɪɴɪɴɢ ᴜs ⚡️~!
❅─────✧❅✦❅✧─────❅**
"""

    return await app.send_message(
        chat_id,
        text,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ",
                        url=(
                            f"https://t.me/"
                            f"{app.username}"
                            f"?startgroup=true"
                        ),
                    )
                ]
            ]
        ),
    )


# ===========================================================
# NEW MEMBER
# ===========================================================

@app.on_chat_member_updated(
    filters.group,
    group=-3,
)
async def greet_new_member(
    _,
    member: ChatMemberUpdated,
):

    chat_id = member.chat.id

    # -------------------------------------------------------
    # CHECK WELCOME STATUS
    # -------------------------------------------------------

    try:

        is_enabled = await get_welcome(
            chat_id
        )

    except Exception as e:

        LOGGER.warning(
            "Could not read welcome status: %s",
            e,
        )

        return

    if not is_enabled:
        return

    # -------------------------------------------------------
    # GET NEW USER
    # -------------------------------------------------------

    if not member.new_chat_member:
        return

    user = member.new_chat_member.user

    if not user:
        return

    # -------------------------------------------------------
    # CHECK NEW MEMBER
    # IMPORTANT:
    # Pyrogram uses BANNED, not KICKED.
    # -------------------------------------------------------

    new_status = member.new_chat_member.status

    # User must currently be a member/restricted member.
    if new_status not in (
        enums.ChatMemberStatus.MEMBER,
        enums.ChatMemberStatus.RESTRICTED,
    ):
        return

    # -------------------------------------------------------
    # CHECK OLD STATUS
    # -------------------------------------------------------

    old_member = member.old_chat_member

    if old_member:

        old_status = old_member.status

        # Don't welcome users whose status was already
        # an active member/admin/restricted member.
        if old_status not in (
            enums.ChatMemberStatus.LEFT,
            enums.ChatMemberStatus.BANNED,
        ):
            return

    # -------------------------------------------------------
    # DELETE PREVIOUS WELCOME
    # -------------------------------------------------------

    old = temp.MELCOW.get(
        f"welcome-{chat_id}"
    )

    if old:

        try:
            await old.delete()
        except Exception:
            pass

    # -------------------------------------------------------
    # GET PROFILE PHOTO
    # -------------------------------------------------------

    pic = "ShiviMusic/assets/upic.png"

    try:

        if user.photo and user.photo.big_file_id:

            downloaded = await app.download_media(
                user.photo.big_file_id,
                file_name=(
                    f"downloads/pp{user.id}.png"
                ),
            )

            if downloaded:
                pic = downloaded

    except Exception as e:

        LOGGER.warning(
            "Could not download profile photo: %s",
            e,
        )

    # -------------------------------------------------------
    # GENERATE WELCOME IMAGE
    # -------------------------------------------------------

    welcomeimg = None

    try:

        welcomeimg = welcomepic(
            pic,
            user.first_name,
            member.chat.title,
            user.id,
            user.username,
        )

    except Exception as e:

        LOGGER.exception(
            "Welcome image generation failed: %s",
            e,
        )

    # -------------------------------------------------------
    # WELCOME TEXT
    # -------------------------------------------------------

    username = (
        f"@{user.username}"
        if user.username
        else "Not Set"
    )

    caption = f"""
**⏤͟͟͞͞★ ʜᴇʟʟᴏ ᴅᴇᴀʀ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ : {member.chat.title}**

<u>**❖ ᴜsᴇʀ sʜᴏʀᴛ ɪɴғᴏ**</u>

**➻ ɴᴀᴍᴇ »** {user.mention}
**➻ ᴄʜᴀᴛ_ɪᴅ »** `{user.id}`
**➻ ᴜ_ɴᴀᴍᴇ »** {username}

**➻ ᴛʜᴀɴᴋs ғᴏʀ ᴊᴏɪɴɪɴɢ ᴜs ⚡️~!
❅─────✧❅✦❅✧─────❅**
"""

    # -------------------------------------------------------
    # BOT GROUP LINK
    # -------------------------------------------------------

    bot_username = getattr(
        app,
        "username",
        None,
    )

    if bot_username:

        bot_url = (
            f"https://t.me/"
            f"{bot_username}"
            f"?startgroup=true"
        )

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ",
                        url=bot_url,
                    )
                ]
            ]
        )

    else:

        keyboard = None

    # -------------------------------------------------------
    # SEND WELCOME
    # -------------------------------------------------------

    msg = None

    if welcomeimg:

        try:

            msg = await app.send_photo(
                chat_id,
                photo=welcomeimg,
                caption=caption,
                reply_markup=keyboard,
            )

        except FloodWait as e:

            LOGGER.warning(
                "FloodWait while sending welcome: %s seconds",
                e.value,
            )

            await asyncio.sleep(
                e.value
            )

            try:

                msg = await app.send_photo(
                    chat_id,
                    photo=welcomeimg,
                    caption=caption,
                    reply_markup=keyboard,
                )

            except Exception as e:

                LOGGER.warning(
                    "Retry welcome photo failed: %s",
                    e,
                )

                msg = None

        except ChatSendPhotosForbidden:

            LOGGER.warning(
                "Photo sending forbidden in chat %s. "
                "Using text welcome.",
                chat_id,
            )

        except ChatWriteForbidden:

            return

        except Exception as e:

            LOGGER.exception(
                "Welcome photo failed: %s",
                e,
            )

    # -------------------------------------------------------
    # TEXT FALLBACK
    # -------------------------------------------------------

    if msg is None:

        try:

            msg = await app.send_message(
                chat_id,
                caption,
                reply_markup=keyboard,
            )

        except FloodWait as e:

            LOGGER.warning(
                "FloodWait while sending text welcome: %s seconds",
                e.value,
            )

            await asyncio.sleep(
                e.value
            )

            try:

                msg = await app.send_message(
                    chat_id,
                    caption,
                    reply_markup=keyboard,
                )

            except Exception as e:

                LOGGER.warning(
                    "Retry text welcome failed: %s",
                    e,
                )

                return

        except ChatWriteForbidden:

            return

        except Exception as e:

            LOGGER.exception(
                "Text welcome failed: %s",
                e,
            )

            return

    # -------------------------------------------------------
    # SAVE CURRENT WELCOME
    # -------------------------------------------------------

    temp.MELCOW[
        f"welcome-{chat_id}"
    ] = msg

    # -------------------------------------------------------
    # AUTO DELETE AFTER 10 SECONDS
    # -------------------------------------------------------

    async def delete_welcome():

        await asyncio.sleep(
            10
        )

        try:

            await msg.delete()

        except Exception:

            pass

        finally:

            if (
                temp.MELCOW.get(
                    f"welcome-{chat_id}"
                )
                == msg
            ):

                temp.MELCOW.pop(
                    f"welcome-{chat_id}",
                    None,
                )

    asyncio.create_task(
        delete_welcome()
    )


# ===========================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder)
#
# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : t.me/Purvi_Bots
# ===========================================================
