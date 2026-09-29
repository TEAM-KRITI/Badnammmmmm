# ============================================================
# 🎧 ᴠɪᴅᴇᴏ ᴄʜᴀᴛ sʏsᴛᴇᴍ
# ShiviMusic
# ============================================================

from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

from ShiviMusic import app


# ============================================================
# 🤖 ʙᴏᴛ ᴜsᴇʀɴᴀᴍᴇ
# ============================================================

async def get_bot_username():
    me = await app.get_me()
    return me.username


# ============================================================
# 🔘 ᴠᴄ ʙᴜᴛᴛᴏɴs
# ============================================================

async def vc_buttons():

    username = await get_bot_username()

    add_link = f"https://t.me/{username}?startgroup=true"

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✙ ᴧᴅᴅ ᴍᴇ ✙",
                    url=add_link,
                ),
                InlineKeyboardButton(
                    " ᴄʟᴏsᴇ ",
                    callback_data="vc_close",
                ),
            ]
        ]
    )


# ============================================================
# 🟢 ᴠɪᴅᴇᴏ ᴄʜᴀᴛ sᴛᴀʀᴛᴇᴅ
# ============================================================

@app.on_message(filters.video_chat_started)
async def vc_started(client, message: Message):

    try:

        chat_name = message.chat.title or "ᴛʜɪs ɢʀᴏᴜᴘ"

        text = (
            f"**❖ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ sᴛᴀʀᴛᴇᴅ ɪɴ {chat_name}**\n\n"
            f"**▶ /play [sᴏɴɢ_ɴᴀᴍᴇ] ᴇɴᴊᴏʏ ᴍᴜsɪᴄ 🎶**"
        )

        buttons = await vc_buttons()

        await message.reply_text(
            text,
            reply_markup=buttons,
            disable_web_page_preview=True,
        )

    except Exception as e:
        print(f"VC START ERROR: {e}")


# ============================================================
# 🔴 ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ᴇɴᴅᴇᴅ
# ============================================================

@app.on_message(filters.video_chat_ended)
async def vc_ended(client, message: Message):

    try:

        chat_name = message.chat.title or "ᴛʜɪs ɢʀᴏᴜᴘ"

        duration_text = ""

        # ----------------------------------------------------
        # ⏱ ᴠᴄ ᴅᴜʀᴀᴛɪᴏɴ
        # ----------------------------------------------------

        try:

            ended = message.video_chat_ended

            if ended and ended.duration:

                total_seconds = ended.duration

                days = total_seconds // 86400
                remaining = total_seconds % 86400

                hours = remaining // 3600
                remaining %= 3600

                minutes = remaining // 60
                seconds = remaining % 60

                if days:
                    duration_text = (
                        f"\n\n**⏰ ᴅᴜʀᴀᴛɪᴏɴ: "
                        f"{days}ᴅ {hours}ʜ**"
                    )

                elif hours:
                    duration_text = (
                        f"\n\n**⏰ ᴅᴜʀᴀᴛɪᴏɴ: "
                        f"{hours}ʜ {minutes}ᴍ**"
                    )

                elif minutes:
                    duration_text = (
                        f"\n\n**⏰ ᴅᴜʀᴀᴛɪᴏɴ: "
                        f"{minutes}ᴍ {seconds}s**"
                    )

                else:
                    duration_text = (
                        f"\n\n**⏰ ᴅᴜʀᴀᴛɪᴏɴ: "
                        f"{seconds}s**"
                    )

        except Exception:
            duration_text = ""

        text = (
            f"**❖ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ᴇɴᴅᴇᴅ ɪɴ {chat_name}**"
            f"{duration_text}\n\n"
            f"**◆ ᴄʟᴇᴀʀᴇᴅ ᴀʟʟ Qᴜᴇᴜᴇ sᴏɴɢs 🗑**"
        )

        buttons = await vc_buttons()

        await message.reply_text(
            text,
            reply_markup=buttons,
            disable_web_page_preview=True,
        )

    except Exception as e:
        print(f"VC END ERROR: {e}")


# ============================================================
# 👥 ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ᴍᴇᴍʙᴇʀs ɪɴᴠɪᴛᴇᴅ
# ============================================================

@app.on_message(filters.video_chat_members_invited)
async def vc_members_invited(client, message: Message):

    try:

        if not message.from_user:
            return

        invited = message.video_chat_members_invited

        if not invited:
            return

        if not invited.users:
            return

        # ----------------------------------------------------
        # 👤 ɪɴᴠɪᴛᴇʀ
        # ----------------------------------------------------

        inviter_name = message.from_user.first_name or "ᴜsᴇʀ"

        inviter = (
            f"[{inviter_name}](tg://user?id={message.from_user.id})"
        )

        # ----------------------------------------------------
        # 👥 ɪɴᴠɪᴛᴇᴅ ᴜsᴇʀs
        # ----------------------------------------------------

        invited_list = []

        for user in invited.users:

            if not user.first_name:
                continue

            invited_list.append(
                f"[{user.first_name}](tg://user?id={user.id})"
            )

        if not invited_list:
            return

        names = ", ".join(invited_list)

        text = (
            f"**❖ {inviter} ɪɴᴠɪᴛᴇᴅ {names} ᴏɴ ᴠᴄ ⚡**\n\n"
            f"**⏤͟͟͞͞★ ᴊᴏɪɴ ғᴀsᴛ & ᴇɴᴊᴏʏ ᴍᴜsɪᴄ 🎧**"
        )

        buttons = await vc_buttons()

        await message.reply_text(
            text,
            reply_markup=buttons,
            disable_web_page_preview=True,
        )

    except Exception as e:
        print(f"VC INVITE ERROR: {e}")


# ============================================================
# ❌ ᴄʟᴏsᴇ ʙᴜᴛᴛᴏɴ
# ============================================================

@app.on_callback_query(filters.regex(r"^vc_close$"))
async def vc_close_callback(client, query: CallbackQuery):

    try:

        await query.answer(
            "ᴍᴇssᴀɢᴇ ᴄʟᴏsᴇᴅ ✨"
        )

        await query.message.delete()

    except Exception as e:

        print(f"VC CLOSE ERROR: {e}")

        try:
            await query.answer(
                "ᴜɴᴀʙʟᴇ ᴛᴏ ᴄʟᴏsᴇ ᴛʜɪs ᴍᴇssᴀɢᴇ.",
                show_alert=True,
            )
        except Exception:
            pass
