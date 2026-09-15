# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots
# =======================================================

import time
import random

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import (
    ChatJoinRequest,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from py_yt import VideosSearch

import config
from ShiviMusic import app
from ShiviMusic.misc import _boot_
from ShiviMusic.plugins.sudo.sudoers import sudoers_list

from ShiviMusic.utils.database import (
    get_served_chats,
    get_served_users,
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)

from ShiviMusic.utils.decorators.language import LanguageStart
from ShiviMusic.utils.formatters import get_readable_time
from ShiviMusic.utils.inline import (
    help_pannel,
    private_panel,
    start_panel,
)

from config import BANNED_USERS
from strings import get_string


# =======================================================
# 🖼️ START PHOTOS
# =======================================================

shivi_PIC = [
    "https://n.uguu.se/COCvZVmH.jpg",
    "https://n.uguu.se/sUnCjERi.jpg",
    "https://h.uguu.se/UFespaut.jpg",
    "https://n.uguu.se/JQCcgtmE.jpg",
    "https://d.uguu.se/SDjTEpEk.jpg",
    "https://n.uguu.se/FzOLVSlF.jpg",
    "https://n.uguu.se/QnLMTcYx.jpg",
    "https://d.uguu.se/aOQGWHbN.jpg",
]


# =======================================================
# 🎧 FIRST START MESSAGE
# =======================================================

def get_start_msg_1(user):
    return (
        f"🎧 <b>𝐇ᴇʏ {user.mention} 👋</b>"
    )


# =======================================================
# 🎶 SECOND START MESSAGE
# =======================================================

def get_start_msg_2(user, bot_name):
    return f"""
✨ <b>𝐖ᴇʟᴄᴏᴍᴇ {user.mention} ❤️</b>

💎 <b>「 {bot_name} 」</b>

🎧 <b>𝐏ʀᴇᴍɪᴜᴍ 𝐐ᴜᴀʟɪᴛʏ
𝐌ᴜsɪᴄ 𝐒ᴛʀᴇᴀᴍɪɴɢ
𝐎ɴ 𝐓ᴇʟᴇɢʀᴀᴍ.</b>

⚡ <b>𝟐𝟒/𝟕 𝐍ᴏɴ-Sᴛᴏᴘ 𝐌ᴜsɪᴄ</b>
🎵 <b>𝐅ᴀsᴛ & 𝐒ᴍᴏᴏᴛʜ 𝐏ʟᴀʏʙᴀᴄᴋ</b>
🔥 <b>𝐙ᴇʀᴏ 𝐋ᴀɢ 𝐄xᴘᴇʀɪᴇɴᴄᴇ</b>
💫 <b>𝐏ʀᴇᴍɪᴜᴍ 𝐌ᴜsɪᴄ 𝐐ᴜᴀʟɪᴛʏ</b>

➤ <b>𝐀ᴅᴅ 𝐌ᴇ 𝐈ɴ 𝐘ᴏᴜʀ 𝐆ʀᴏᴜᴘ 🚀</b>

🎶 <b>𝐋ᴇᴛ 𝐓ʜᴇ 𝐌ᴜsɪᴄ
𝐍ᴇᴠᴇʀ 𝐒ᴛᴏᴘ ❤️</b>
"""


# =======================================================
# 🔘 PRIVATE START BUTTONS
# =======================================================

START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="➕ 𝐀ᴅᴅ 𝐌ᴇ 𝐈ɴ 𝐘ᴏᴜʀ 𝐆ʀᴏᴜᴘ",
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(
                text="🛒 𝐁ᴜʏ 𝐓ɢ 𝐀ᴄᴄᴏᴜɴᴛ ↗",
                url="https://t.me/YourUsername",
            )
        ],
    ]
)


# =======================================================
# 📩 PRIVATE /START
# =======================================================

@app.on_message(
    filters.command(["start"])
    & filters.private
    & ~BANNED_USERS
)
@LanguageStart
async def start_pm(
    client,
    message: Message,
    _,
):

    user = message.from_user

    if not user:
        return

    # ===================================================
    # ADD USER
    # ===================================================

    await add_served_user(user.id)

    # ===================================================
    # DELETE /START
    # ===================================================

    try:
        await message.delete()
    except Exception:
        pass

    # ===================================================
    # START ARGUMENT
    # ===================================================

    if len(message.text.split()) > 1:

        name = message.text.split(None, 1)[1]

        # ------------------------------------------------
        # HELP
        # ------------------------------------------------

        if name.startswith("help"):

            keyboard = help_pannel(_)

            return await message.reply_photo(
                random.choice(shivi_PIC),
                caption=_["help_1"].format(
                    config.SUPPORT_CHAT
                ),
                reply_markup=keyboard,
            )

        # ------------------------------------------------
        # SUDO LIST
        # ------------------------------------------------

        if name.startswith("sud"):

            await sudoers_list(
                client=client,
                message=message,
                _=_,
            )

            if await is_on_off(2):

                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=(
                        f"✦ {user.mention} "
                        f"ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ "
                        f"<b>sᴜᴅᴏʟɪsᴛ</b>.\n\n"

                        f"<b>✦ ᴜsᴇʀ ɪᴅ ➠</b> "
                        f"<code>{user.id}</code>\n"

                        f"<b>✦ ᴜsᴇʀɴᴀᴍᴇ ➠</b> "
                        f"@{user.username or 'None'}"
                    ),
                )

            return

        # ------------------------------------------------
        # YOUTUBE INFO
        # ------------------------------------------------

        if name.startswith("inf"):

            m = await message.reply_text("🔎")

            query = name.replace(
                "info_",
                "",
                1,
            )

            query = (
                f"https://www.youtube.com/watch?v={query}"
            )

            try:

                results = VideosSearch(
                    query,
                    limit=1,
                )

                data = await results.next()

                if not data.get("result"):
                    await m.edit_text(
                        "❌ <b>Video information not found.</b>"
                    )
                    return

                result = data["result"][0]

                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]

                thumbnail = (
                    result["thumbnails"][0]["url"]
                    .split("?")[0]
                )

                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]

                searched_text = _["start_6"].format(
                    title,
                    duration,
                    views,
                    published,
                    channellink,
                    channel,
                    app.mention,
                )

                key = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=_["S_B_8"],
                                url=link,
                            ),
                            InlineKeyboardButton(
                                text=_["S_B_9"],
                                url=config.SUPPORT_CHAT,
                            ),
                        ],
                    ]
                )

                await m.delete()

                await app.send_photo(
                    chat_id=message.chat.id,
                    photo=thumbnail,
                    caption=searched_text,
                    reply_markup=key,
                )

                if await is_on_off(2):

                    return await app.send_message(
                        chat_id=config.LOGGER_ID,
                        text=(
                            f"✦ {user.mention} "
                            f"ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ "
                            f"ᴛᴏ ᴄʜᴇᴄᴋ "
                            f"<b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n"

                            f"✦ <b>ᴜsᴇʀ ɪᴅ ➠</b> "
                            f"<code>{user.id}</code>\n"

                            f"✦ <b>ᴜsᴇʀɴᴀᴍᴇ ➠</b> "
                            f"@{user.username or 'None'}"
                        ),
                    )

            except Exception as ex:

                try:
                    await m.edit_text(
                        "❌ <b>Unable to fetch video information.</b>"
                    )
                except Exception:
                    pass

                print(
                    f"[START INFO] {ex}"
                )

            return

        return

    # ===================================================
    # 🌸 NORMAL PRIVATE START
    # ===================================================

    # ---------------------------------------------------
    # BOT NAME
    # ---------------------------------------------------

    bot_name = app.first_name

    # ---------------------------------------------------
    # MESSAGE 1
    # ---------------------------------------------------

    await app.send_message(
        chat_id=message.chat.id,
        text=get_start_msg_1(user),
    )

    # ---------------------------------------------------
    # MESSAGE 2
    # ---------------------------------------------------

    await app.send_photo(
        chat_id=message.chat.id,
        photo=random.choice(shivi_PIC),
        has_spoiler=True,
        caption=get_start_msg_2(
            user,
            bot_name,
        ),
        reply_markup=START_BUTTONS,
    )

    # ===================================================
    # 📝 LOGGER
    # ===================================================

    if await is_on_off(2):

        return await app.send_message(
            chat_id=config.LOGGER_ID,
            text=(
                f"✦ {user.mention} "
                f"ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n"

                f"<b>ᴜsᴇʀ ɪᴅ :</b> "
                f"<code>{user.id}</code>\n"

                f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> "
                f"@{user.username or 'None'}"
            ),
        )


# =======================================================
# 📩 JOIN REQUEST → PRIVATE WELCOME
# =======================================================

@app.on_chat_join_request()
async def join_request_welcome(
    client,
    request: ChatJoinRequest,
):

    user = request.from_user

    if not user:
        return

    try:

        language = await get_lang(
            request.chat.id
        )

        _ = get_string(language)

        user_chat_id = (
            getattr(
                request,
                "user_chat_id",
                None,
            )
            or user.id
        )

        group_title = (
            request.chat.title
            or "ᴛʜɪs ɢʀᴏᴜᴘ"
        )

        # =================================================
        # ✨ PREMIUM WELCOME
        # =================================================

        caption = (
            f"<b>🌸 ᴡᴇʟᴄᴏᴍᴇ, {user.mention} 🇮🇳</b>\n\n"

            f"✨ ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴊᴏɪɴ "
            f"<b>{group_title}</b> "
            f"ʜᴀs ʙᴇᴇɴ ʀᴇᴄᴇɪᴠᴇᴅ. ✅\n\n"

            f"💎 <b>ᴛʜᴀɴᴋ ʏᴏᴜ ғᴏʀ ᴄʜᴏᴏsɪɴɢ "
            f"{app.mention}</b>\n\n"

            f"🎶 ᴇɴᴊᴏʏ ʜɪɢʜ-ǫᴜᴀʟɪᴛʏ ᴍᴜsɪᴄ "
            f"ᴡɪᴛʜ {app.mention}. ✨\n\n"

            f"🎧 • ʜɪɢʜ ǫᴜᴀʟɪᴛʏ ᴍᴜsɪᴄ\n"
            f"⚡ • ғᴀsᴛ & sᴍᴏᴏᴛʜ ᴘʟᴀʏʙᴀᴄᴋ\n"
            f"💫 • ᴘʀᴇᴍɪᴜᴍ ᴍᴜsɪᴄ ᴇxᴘᴇʀɪᴇɴᴄᴇ\n\n"

            f"🔔 <b>ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ɪs ᴘᴇɴᴅɪɴɢ.</b>\n"
            f"⏳ ᴡᴀɪᴛ ғᴏʀ ᴀᴅᴍɪɴ ᴀᴘᴘʀᴏᴠᴀʟ. ❤️\n\n"

            f"🤖 <b>sᴛᴀʀᴛ {app.mention}</b> "
            f"ᴡɪᴛʜ <b>/start</b> 🎵\n\n"

            f"✨ ᴇɴᴊᴏʏ ᴛʜᴇ ᴍᴜsɪᴄ • "
            f"ᴇɴᴊᴏʏ ᴛʜᴇ ᴠɪʙᴇ ✨"
        )

        # =================================================
        # 🔘 BUTTONS
        # =================================================

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=_["S_B_14"],
                        callback_data="abot_cb",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=_["S_B_6"],
                        url=config.SUPPORT_CHANNEL,
                    ),
                    InlineKeyboardButton(
                        text=_["S_B_9"],
                        url=config.SUPPORT_CHAT,
                    ),
                ],
            ]
        )

        # =================================================
        # 📤 SEND WELCOME
        # =================================================

        await app.send_photo(
            chat_id=user_chat_id,
            photo=random.choice(shivi_PIC),
            has_spoiler=True,
            caption=caption,
            reply_markup=keyboard,
        )

    except Exception as ex:

        print(
            f"[JOIN REQUEST] {ex}"
        )


# =======================================================
# 👥 GROUP /START
# =======================================================

@app.on_message(
    filters.command(["start"])
    & filters.group
    & ~BANNED_USERS
)
@LanguageStart
async def start_gp(
    client,
    message: Message,
    _,
):

    out = start_panel(_)

    uptime = int(
        time.time() - _boot_
    )

    await message.reply_photo(
        random.choice(shivi_PIC),
        has_spoiler=True,
        caption=_["start_1"].format(
            app.mention,
            get_readable_time(uptime),
        ),
        reply_markup=InlineKeyboardMarkup(out),
    )

    return await add_served_chat(
        message.chat.id
    )


# =======================================================
# 👋 NEW MEMBER WELCOME
# =======================================================

@app.on_message(
    filters.new_chat_members,
    group=-1,
)
async def welcome(
    client,
    message: Message,
):

    for member in message.new_chat_members:

        try:

            language = await get_lang(
                message.chat.id
            )

            _ = get_string(language)

            # ---------------------------------------------
            # BANNED USER CHECK
            # ---------------------------------------------

            if await is_banned_user(member.id):

                try:
                    await message.chat.ban_member(
                        member.id
                    )
                except Exception:
                    pass

            # ---------------------------------------------
            # BOT ADDED
            # ---------------------------------------------

            if member.id == app.id:

                # -----------------------------------------
                # SUPERGROUP CHECK
                # -----------------------------------------

                if (
                    message.chat.type
                    != ChatType.SUPERGROUP
                ):

                    await message.reply_text(
                        _["start_4"]
                    )

                    return await app.leave_chat(
                        message.chat.id
                    )

                # -----------------------------------------
                # BLACKLIST CHECK
                # -----------------------------------------

                if (
                    message.chat.id
                    in await blacklisted_chats()
                ):

                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            (
                                f"https://t.me/"
                                f"{app.username}"
                                f"?start=sudolist"
                            ),
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )

                    return await app.leave_chat(
                        message.chat.id
                    )

                # -----------------------------------------
                # BOT WELCOME
                # -----------------------------------------

                out = start_panel(_)

                await message.reply_text(
                    text=_["start_3"].format(
                        message.from_user.mention,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        out
                    ),
                )

                await add_served_chat(
                    message.chat.id
                )

                await message.stop_propagation()

        except Exception as ex:

            print(
                f"[WELCOME] {ex}"
            )


# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots
# =======================================================
