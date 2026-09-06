# -----------------------------------------------
# 🔸 CharviMusic Project
# 🔹 Developed & Maintained by: Charvi Bots
# 📅 Copyright © 2022 – All Rights Reserved
# -----------------------------------------------

import random

from pyrogram import filters, enums
from ShiviMusic import app

from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    ChatPermissions,
)

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ShiviMusic.utils.nightmodedb import (
    nightdb,
    nightmode_on,
    nightmode_off,
    get_nightchats,
)


# =======================================================
# CHAT PERMISSIONS
# =======================================================

CLOSE_CHAT = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_polls=False,
    can_change_info=False,
    can_add_web_page_previews=False,
    can_pin_messages=False,
    can_invite_users=False
)

OPEN_CHAT = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=True,
    can_add_web_page_previews=True,
    can_pin_messages=True,
    can_invite_users=True
)


# =======================================================
# NIGHTMODE BUTTONS
# =======================================================

buttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "๏ ᴇηᴧʙʟᴇ ๏",
                callback_data="add_night"
            ),
            InlineKeyboardButton(
                "๏ ᴅɪѕᴧʙʟᴇ ๏",
                callback_data="rm_night"
            )
        ]
    ]
)


# =======================================================
# ADD BOT BUTTON
# =======================================================

NIGHT_MSG_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "ᴧᴅᴅ мᴇ ɪη ʏσυʀ ɢʀσυᴘ",
                url=f"https://t.me/{app.username}?startgroup=true"
            )
        ]
    ]
)


# =======================================================
# NIGHTMODE COMMAND
# =======================================================

@app.on_message(filters.command("nightmode") & filters.group)
async def _nightmode(_, message):

    return await message.reply_photo(
        photo="https://n.uguu.se/PbzKsnAJ.jpg",

        caption=(
            "**⚙️ ɴɪɢнᴛмσᴅᴇ ѕᴇᴛᴛɪηɢѕ**\n\n"
            "**ᴄʟɪᴄκ ᴛнᴇ ʙυᴛᴛσηѕ ʙᴇʟσω ᴛσ ᴄσηᴛʀσʟ "
            "ɴɪɢнᴛмσ∂ᴇ ѕᴇᴛᴛɪηɢѕ ғσʀ ᴛнɪѕ ɢʀσυᴘ.**"
        ),

        parse_mode=enums.ParseMode.MARKDOWN,
        reply_markup=buttons
    )


# =======================================================
# NIGHTMODE CALLBACK
# =======================================================

@app.on_callback_query(
    filters.regex("^(add_night|rm_night)$")
)
async def nightcb(_, query: CallbackQuery):

    data = query.data
    chat_id = query.message.chat.id
    user_id = query.from_user.id

    check_night = await nightdb.find_one(
        {"chat_id": chat_id}
    )

    administrators = []

    async for m in app.get_chat_members(
        chat_id,
        filter=enums.ChatMembersFilter.ADMINISTRATORS
    ):
        administrators.append(m.user.id)

    if user_id not in administrators:
        return await query.answer(
            "❌ σηʟʏ ᴧᴅмɪηѕ ᴄᴧη υѕᴇ ᴛнɪѕ ᴄσммᴧηᴅ!",
            show_alert=True
        )

    # ===================================================
    # ENABLE
    # ===================================================

    if data == "add_night":

        if check_night:

            await query.message.edit_caption(
                caption=(
                    "**🌕 ɴɪɢнᴛмσᴅᴇ ɪѕ ᴧʟʀᴇᴧᴅʏ "
                    "ᴇηᴧʙʟᴇ∂ ɪη ᴛнɪѕ ɢʀσυᴘ.**"
                ),
                parse_mode=enums.ParseMode.MARKDOWN,
                reply_markup=buttons
            )

        else:

            await nightmode_on(chat_id)

            await query.message.edit_caption(
                caption=(
                    "**✅ ɴɪɢнᴛмσᴅᴇ ᴧᴄᴛɪνᴧᴛᴇᴅ!**\n\n"
                    "**ᴛнɪѕ ɢʀσυᴘ ᴡɪʟʟ ᴧυᴛσмᴧᴛɪᴄᴧʟʟʏ "
                    "ʟσᴄκ ᴧᴛ 𝟏𝟐:𝟎𝟎 ᴧм & υηʟσᴄκ ᴧᴛ "
                    "𝟎𝟔:𝟎𝟎 ᴧм [ɪѕᴛ].**"
                ),
                parse_mode=enums.ParseMode.MARKDOWN,
                reply_markup=buttons
            )

    # ===================================================
    # DISABLE
    # ===================================================

    elif data == "rm_night":

        if check_night:

            await nightmode_off(chat_id)

            await query.message.edit_caption(
                caption="**❌ ɴɪɢнᴛмσᴅᴇ ᴅᴇᴧᴄᴛɪνᴧᴛᴇᴅ!**",
                parse_mode=enums.ParseMode.MARKDOWN,
                reply_markup=buttons
            )

        else:

            await query.message.edit_caption(
                caption=(
                    "**🌑 ɴɪɢнᴛмσᴅᴇ ɪѕ ᴧʟʀᴇᴧᴅʏ "
                    "ᴛυʀηᴇ∂ σғғ.**"
                ),
                parse_mode=enums.ParseMode.MARKDOWN,
                reply_markup=buttons
            )

    await query.answer()


# =======================================================
# GOOD NIGHT
# =======================================================

async def start_nightmode():

    schats = await get_nightchats()

    for chat in schats:

        chat_id = int(chat["chat_id"])

        try:

            group = await app.get_chat(chat_id)

            group_name = group.title or "υηκɴσωη ɢʀσυᴘ"

            await app.send_photo(
                chat_id,

                photo="https://d.uguu.se/agsYnJwN.jpg",

                caption=(
                    "**🌌 ɢσσᴅ ɴɪɢнᴛ ᴇνᴇʀʏσηᴇ!**\n"
                    "**━─────────────────━**\n\n"

                    "**✨ ᴛɪмᴇ ᴛσ ᴛυʀη σғғ ʏσυʀ ѕᴄʀᴇᴇηѕ "
                    "ᴧηᴅ ᴄᴧᴛᴄн ѕσмᴇ ᴘᴇᴧᴄᴇғυʟ ᴅʀᴇᴧмѕ. "
                    "мᴧʏ ʏσυʀ ѕʟᴇᴇᴘ ʙᴇ ѕᴡᴇᴇᴛ ᴧηᴅ "
                    "ʀᴇѕᴛғυʟ.**\n\n"

                    "**🔒 ɢʀσυᴘ ɪѕ ησω ᴄʟσѕᴇᴅ.**\n\n"

                    "**• ησ мᴇѕѕᴧɢᴇѕ ᴄᴧη ʙᴇ ѕᴇηᴛ "
                    "υηᴛɪʟ мσʀηɪηɢ. ѕᴇᴇ ʏσυ ᴧʟʟ "
                    "ᴛσмσʀʀσω!**\n\n"

                    f"**👥 ɢʀσυᴘ ηᴧмᴇ : {group_name}**\n"
                    f"**🆔 ɢʀσυᴘ ɪᴅ : `{chat_id}`**\n\n"

                    "**⚡ ᴘσωᴇʀᴇᴅ ʙʏ : "
                    "[κɪʀᴛɪ мυѕɪᴄ](https://t.me/annu_updates)**"
                ),

                parse_mode=enums.ParseMode.MARKDOWN,
                reply_markup=NIGHT_MSG_BUTTONS
            )

            await app.set_chat_permissions(
                chat_id,
                CLOSE_CHAT
            )

        except Exception as e:

            print(
                f"Unable to close group {chat_id}: {e}"
            )


# =======================================================
# GOOD MORNING
# =======================================================

async def close_nightmode():

    schats = await get_nightchats()

    for chat in schats:

        chat_id = int(chat["chat_id"])

        try:

            group = await app.get_chat(chat_id)

            group_name = group.title or "υηκɴσωη ɢʀσυᴘ"

            await app.send_photo(
                chat_id,

                photo="https://n.uguu.se/ulpfbxJW.jpg",

                caption=(
                    "**🌅 ɢσσᴅ мσʀηɪηɢ ᴇνᴇʀʏσηᴇ..!**\n"
                    "**━─────────────────━**\n\n"

                    "**✨ ᴧ ʙᴇᴧυᴛɪғυʟ ηᴇᴡ ᴅᴧʏ нᴧѕ "
                    "ᴧʀʀɪνᴇᴅ. мᴧʏ ᴛнɪѕ ᴅᴧʏ ʙʀɪηɢ "
                    "ᴇηᴅʟᴇѕѕ σᴘᴘσʀᴛυηɪᴛɪᴇѕ, ᴊσʏ, ᴧη∂ "
                    "ѕυᴄᴄᴇѕѕ ᴛσ ʏσυʀ ʟɪғᴇ.**\n\n"

                    "**🔓 ɢʀσυᴘ ɪѕ ησω σᴘᴇη.**\n\n"

                    "**• ғᴇᴇʟ ғʀᴇᴇ ᴛσ ᴄнᴧᴛ, ѕнᴧʀᴇ, ᴧηᴅ "
                    "ѕᴛᴧʏ ᴘσѕɪᴛɪνᴇ!**\n\n"

                    f"**👥 ɢʀσυᴘ ηᴧмᴇ : {group_name}**\n"
                    f"**🆔 ɢʀσυᴘ ɪᴅ : `{chat_id}`**\n\n"

                    "**⚡ ᴘσωᴇʀᴇᴅ ʙʏ : "
                    "[κɪʀᴛɪ мυѕɪᴄ](https://t.me/annu_updates)**"
                ),

                parse_mode=enums.ParseMode.MARKDOWN,
                reply_markup=NIGHT_MSG_BUTTONS
            )

            await app.set_chat_permissions(
                chat_id,
                OPEN_CHAT
            )

        except Exception as e:

            print(
                f"Unable to open group {chat_id}: {e}"
            )


# =======================================================
# SCHEDULER
# =======================================================

scheduler = AsyncIOScheduler(
    timezone="Asia/Kolkata"
)

# 11:59 PM
scheduler.add_job(
    start_nightmode,
    trigger="cron",
    hour=23,
    minute=59
)

# 06:01 AM
scheduler.add_job(
    close_nightmode,
    trigger="cron",
    hour=6,
    minute=1
)

scheduler.start()


# =======================================================
# ©️ 2025-26 CharviMusic
# =======================================================
