# -----------------------------------------------
# 🔸 CharviMusic Project
# 🔹 Developed & Maintained by: Charvi Bots
# 📅 Copyright © 2022 – All Rights Reserved
# -----------------------------------------------

from html import escape

from pyrogram import filters, enums
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    ChatPermissions,
)

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ShiviMusic import app

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

@app.on_message(
    filters.command("nightmode") & filters.group
)
async def _nightmode(_, message):

    await message.reply_photo(
        photo="https://n.uguu.se/PbzKsnAJ.jpg",

        caption=(
            "<b>⚙️ ɴɪɢнᴛмσᴅᴇ ѕᴇᴛᴛɪηɢѕ</b>\n\n"
            "<b>ᴄʟɪᴄκ ᴛнᴇ ʙυᴛᴛσηѕ ʙᴇʟσω ᴛσ ᴄσηᴛʀσʟ "
            "ɴɪɢнᴛмσᴅᴇ ѕᴇᴛᴛɪηɢѕ ғσʀ ᴛнɪѕ ɢʀσυᴘ.</b>\n\n"
            "<b>🌙 ɴɪɢнᴛмσᴅᴇ ᴛɪмᴇ:</b>\n"
            "<b>🌆 06:00 PM → 🌅 06:00 AM [IST]</b>\n\n"
            "<b>👑 σηʟʏ ɢʀσυᴘ σωηᴇʀ ᴄᴧη ѕᴇηᴅ "
            "мᴇѕѕᴧɢᴇѕ ᴅυʀɪηɢ ηɪɢнᴛмσᴅᴇ.</b>"
        ),

        parse_mode=enums.ParseMode.HTML,
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

    try:

        async for member in app.get_chat_members(
            chat_id,
            filter=enums.ChatMembersFilter.ADMINISTRATORS
        ):
            administrators.append(member.user.id)

    except Exception as e:

        print(f"Admin check error: {e}")

        return await query.answer(
            "❌ Unable to check administrators!",
            show_alert=True
        )

    # Only admins can use buttons
    if user_id not in administrators:

        return await query.answer(
            "❌ σηʟʏ ᴧᴅмɪηѕ ᴄᴧη υѕᴇ ᴛнɪѕ!",
            show_alert=True
        )


    # ===================================================
    # ENABLE
    # ===================================================

    if data == "add_night":

        if check_night:

            await query.message.edit_caption(
                caption=(
                    "<b>🌕 ɴɪɢнᴛмσᴅᴇ ɪѕ ᴧʟʀᴇᴧᴅʏ "
                    "ᴇηᴧʙʟᴇᴅ ɪη ᴛнɪѕ ɢʀσυᴘ.</b>\n\n"
                    "<b>⏰ 06:00 PM → 06:00 AM [IST]</b>\n"
                    "<b>👑 σηʟʏ σωηᴇʀ ᴄᴧη ѕᴇηᴅ.</b>"
                ),
                parse_mode=enums.ParseMode.HTML,
                reply_markup=buttons
            )

        else:

            await nightmode_on(chat_id)

            await query.message.edit_caption(
                caption=(
                    "<b>✅ ɴɪɢнᴛмσᴅᴇ ᴧᴄᴛɪνᴧᴛᴇᴅ!</b>\n\n"
                    "<b>🌙 ɴɪɢнᴛмσᴅᴇ: "
                    "06:00 PM → 06:00 AM [IST]</b>\n\n"
                    "<b>👑 σηʟʏ ɢʀσυᴘ σωηᴇʀ ᴄᴧη "
                    "ѕᴇηᴅ мᴇѕѕᴧɢᴇѕ.</b>\n"
                    "<b>🔴 Admins & members' messages will be deleted.</b>"
                ),
                parse_mode=enums.ParseMode.HTML,
                reply_markup=buttons
            )


    # ===================================================
    # DISABLE
    # ===================================================

    elif data == "rm_night":

        if check_night:

            await nightmode_off(chat_id)

            await query.message.edit_caption(
                caption=(
                    "<b>❌ ɴɪɢнᴛмσᴅᴇ ᴅᴇᴧᴄᴛɪνᴧᴛᴇᴅ!</b>\n\n"
                    "<b>🌅 ɢʀσυᴘ ɪѕ ησω σηᴇη ғσʀ ᴇνᴇʀʏσηᴇ.</b>"
                ),
                parse_mode=enums.ParseMode.HTML,
                reply_markup=buttons
            )

        else:

            await query.message.edit_caption(
                caption=(
                    "<b>🌑 ɴɪɢнᴛмσᴅᴇ ɪѕ ᴧʟʀᴇᴧᴅʏ "
                    "ᴛυʀηᴇᴅ σғғ.</b>"
                ),
                parse_mode=enums.ParseMode.HTML,
                reply_markup=buttons
            )

    await query.answer()


# =======================================================
# OWNER ONLY MESSAGE SYSTEM
# =======================================================

@app.on_message(
    filters.group
    & ~filters.service
)
async def nightmode_owner_only(_, message):

    chat_id = message.chat.id

    # Check Night Mode database
    night_enabled = await nightdb.find_one(
        {"chat_id": chat_id}
    )

    if not night_enabled:
        return

    # Ignore messages without user
    if not message.from_user:
        return

    user_id = message.from_user.id

    try:

        member = await app.get_chat_member(
            chat_id,
            user_id
        )

        # =================================================
        # ONLY OWNER CAN SEND
        # =================================================

        if member.status == enums.ChatMemberStatus.OWNER:
            return

        # =================================================
        # DELETE EVERYONE ELSE
        # =================================================

        await message.delete()

    except Exception as e:

        print(
            f"NightMode message delete error "
            f"[{chat_id}]: {e}"
        )


# =======================================================
# GOOD NIGHT — 06:00 PM
# =======================================================

async def start_nightmode():

    schats = await get_nightchats()

    for chat in schats:

        chat_id = int(chat["chat_id"])

        try:

            group = await app.get_chat(chat_id)

            group_name = escape(
                group.title or "υηκɴσωη ɢʀσυᴘ"
            )

            # Lock group first
            await app.set_chat_permissions(
                chat_id,
                CLOSE_CHAT
            )

            caption = (
                "<u><b>🌙 ɴɪɢнᴛмσᴅᴇ ѕᴛᴧʀᴛᴇᴅ — "
                "ɢʀσυᴘ ᴄʟσѕᴇᴅ.</b></u>\n\n"

                "<b>◉ ηση-σωηᴇʀѕ ᴄᴧη'ᴛ ѕᴇηᴅ "
                "мᴇѕѕᴧɢᴇѕ ησω.</b>\n"

                "<b>◉ 👑 σηʟʏ ɢʀσυᴘ σωηᴇʀ "
                "ᴄᴧη ѕᴇηᴅ.</b>\n"

                "<b>◉ ɢσσᴅ ηɪɢнᴛ ᴇνᴇʀʏσηᴇ 🌙</b>\n\n"

                f"<b>✧ ɢʀσυᴘ ηᴧмᴇ : {group_name}</b>\n"
                f"<b>✧ ɢʀσυᴘ ɪᴅ : <code>{chat_id}</code></b>\n\n"

                "<b>◎ ᴘσωᴇʀᴇᴅ ʙʏ : "
                "<a href='https://t.me/annu_updates'>"
                "κɪʀᴛɪ ϟ мυѕɪᴄ</a> ♪</b>"
            )

            await app.send_photo(
                chat_id,
                photo="https://d.uguu.se/agsYnJwN.jpg",
                caption=caption,
                parse_mode=enums.ParseMode.HTML,
                reply_markup=NIGHT_MSG_BUTTONS
            )

        except Exception as e:

            print(
                f"Unable to close group {chat_id}: {e}"
            )


# =======================================================
# GOOD MORNING — 06:00 AM
# =======================================================

async def close_nightmode():

    schats = await get_nightchats()

    for chat in schats:

        chat_id = int(chat["chat_id"])

        try:

            group = await app.get_chat(chat_id)

            group_name = escape(
                group.title or "υηκɴσωη ɢʀσυᴘ"
            )

            # Open group first
            await app.set_chat_permissions(
                chat_id,
                OPEN_CHAT
            )

            caption = (
                "<u><b>🌅 ɴɪɢнᴛмσᴅᴇ ᴇηᴅᴇᴅ — "
                "ɢʀσυᴘ σᴘᴇη.</b></u>\n\n"

                "<b>◉ ᴇνᴇʀʏσηᴇ ᴄᴧη ησω ѕᴇηᴅ "
                "мᴇѕѕᴧɢᴇѕ.</b>\n"

                "<b>◉ ɢσσᴅ мσʀηɪηɢ ᴇνᴇʀʏσηᴇ ☀️</b>\n\n"

                f"<b>✧ ɢʀσυᴘ ηᴧмᴇ : {group_name}</b>\n"
                f"<b>✧ ɢʀσυᴘ ɪᴅ : <code>{chat_id}</code></b>\n\n"

                "<b>◎ ᴘσωᴇʀᴇᴅ ʙʏ : "
                "<a href='https://t.me/annu_updates'>"
                "κɪʀᴛɪ ϟ мυѕɪᴄ</a> ♪</b>"
            )

            await app.send_photo(
                chat_id,
                photo="https://n.uguu.se/ulpfbxJW.jpg",
                caption=caption,
                parse_mode=enums.ParseMode.HTML,
                reply_markup=NIGHT_MSG_BUTTONS
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


# =======================================================
# 🌙 06:00 PM — NIGHT MODE START
# =======================================================

scheduler.add_job(
    start_nightmode,
    trigger="cron",
    hour=18,
    minute=0,
    id="nightmode_start",
    replace_existing=True
)


# =======================================================
# 🌅 06:00 AM — NIGHT MODE END
# =======================================================

scheduler.add_job(
    close_nightmode,
    trigger="cron",
    hour=6,
    minute=0,
    id="nightmode_end",
    replace_existing=True
)


# =======================================================
# START SCHEDULER
# =======================================================

if not scheduler.running:
    scheduler.start()


# =======================================================
# ©️ 2025-26 CharviMusic
# =======================================================
