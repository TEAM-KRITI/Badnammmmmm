# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder)
# =======================================================

import time
import random

from pyrogram import filters
from pyrogram.enums import ChatType, ParseMode
from pyrogram.types import (
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


# =========================================================
# START / WELCOME IMAGES
# =========================================================

shivi_PIC = [
    "https://files.catbox.moe/4ojtc4.jpg",
    "https://files.catbox.moe/30wg78.jpg",
    "https://files.catbox.moe/4ojtc4.jpg",
    "https://files.catbox.moe/30wg78.jpg",
]


# =========================================================
# PRIVATE GROUP JOIN REQUEST
# =========================================================

@app.on_chat_join_request()
async def join_request_welcome(client, request):

    try:
        user = request.from_user
        chat = request.chat

        if not user:
            return

        # -------------------------------------------------
        # CURRENT BOT DETAILS
        # -------------------------------------------------

        me = await client.get_me()

        bot_name = me.first_name or "ᴍᴜsɪᴄ ʙᴏᴛ"
        bot_username = me.username

        if bot_username:
            bot_display = f"@{bot_username}"
            bot_url = f"https://t.me/{bot_username}"
        else:
            bot_display = bot_name
            bot_url = config.SUPPORT_CHAT

        # -------------------------------------------------
        # USER / GROUP
        # -------------------------------------------------

        user_name = user.first_name or "ᴜsᴇʀ"
        group_name = chat.title or "ᴘʀɪᴠᴀᴛᴇ ɢʀᴏᴜᴘ"

        # -------------------------------------------------
        # UPDATE / SUPPORT
        # -------------------------------------------------

        update_url = getattr(
            config,
            "UPDATE_CHAT",
            config.SUPPORT_CHAT,
        )

        support_url = getattr(
            config,
            "SUPPORT_CHAT",
            update_url,
        )

        # -------------------------------------------------
        # ADVANCED FONT + BOLD MESSAGE
        # -------------------------------------------------

        welcome_text = f"""
<b>ᴡᴇʟᴄᴏᴍᴇ, {user_name}!</b>

<b>ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴊᴏɪɴ {group_name} ʜᴀs ʙᴇᴇɴ ʀᴇᴄᴇɪᴠᴇᴅ.</b>

<b>ᴡʜɪʟᴇ ʏᴏᴜ ᴡᴀɪᴛ, ᴇxᴘʟᴏʀᴇ {bot_display} 🎵.</b>

<b>• ʜɪɢʜ ǫᴜᴀʟɪᴛʏ ᴍᴜsɪᴄ</b>
<b>• ғᴀsᴛ &amp; sᴍᴏᴏᴛʜ ᴘʟᴀʏʙᴀᴄᴋ</b>
<b>• sᴛᴀʙʟᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ</b>

<b>ᴜsᴇ /sᴛᴀʀᴛ ᴛᴏ ʙᴇɢɪɴ.</b>
"""

        # -------------------------------------------------
        # BUTTONS
        # -------------------------------------------------

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "↗ ᴍᴏʀᴇ ɪɴғᴏ",
                        url=bot_url,
                    )
                ],
                [
                    InlineKeyboardButton(
                        "ᴜᴘᴅᴀᴛᴇ ↗",
                        url=update_url,
                    ),
                    InlineKeyboardButton(
                        "sᴜᴘᴘᴏʀᴛ ↗",
                        url=support_url,
                    ),
                ],
            ]
        )

        # -------------------------------------------------
        # SEND MESSAGE
        # -------------------------------------------------

        await client.send_photo(
            chat_id=request.user_chat_id,
            photo=random.choice(shivi_PIC),
            caption=welcome_text,
            reply_markup=buttons,
            parse_mode=ParseMode.HTML,
        )

        # -------------------------------------------------
        # LOGGER
        # -------------------------------------------------

        if await is_on_off(2):

            username = (
                f"@{user.username}"
                if user.username
                else "ɴᴏ ᴜsᴇʀɴᴀᴍᴇ"
            )

            logger_text = f"""
<b>✦ ɴᴇᴡ ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ</b>

<b>✦ ᴜsᴇʀ ➜</b> {user.mention}
<b>✦ ᴜsᴇʀ ɪᴅ ➜</b> <code>{user.id}</code>
<b>✦ ᴜsᴇʀɴᴀᴍᴇ ➜</b> {username}

<b>✦ ɢʀᴏᴜᴘ ➜</b> {group_name}
<b>✦ ᴄʜᴀᴛ ɪᴅ ➜</b> <code>{chat.id}</code>

<b>✦ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇ sᴇɴᴛ ✓</b>
"""

            await client.send_message(
                chat_id=config.LOGGER_ID,
                text=logger_text,
                parse_mode=ParseMode.HTML,
            )

    except Exception as ex:

        print(
            f"[ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ ᴇʀʀᴏʀ] {ex}"
        )


# =========================================================
# PRIVATE /START
# =========================================================

@app.on_message(
    filters.command(["start"])
    & filters.private
    & ~BANNED_USERS
)
@LanguageStart
async def start_pm(client, message: Message, _):

    await add_served_user(
        message.from_user.id
    )

    try:
        await message.delete()
    except Exception:
        pass

    # =====================================================
    # START PARAMETER
    # =====================================================

    if len(message.text.split()) > 1:

        name = message.text.split(
            None,
            1
        )[1]

        # -------------------------------------------------
        # HELP
        # -------------------------------------------------

        if name[0:4] == "help":

            keyboard = help_pannel(_)

            return await message.reply_photo(
                random.choice(shivi_PIC),
                caption=_["help_1"].format(
                    config.SUPPORT_CHAT
                ),
                reply_markup=keyboard,
            )

        # -------------------------------------------------
        # SUDO
        # -------------------------------------------------

        if name[0:3] == "sud":

            await sudoers_list(
                client=client,
                message=message,
                _=_,
            )

            if await is_on_off(2):

                username = (
                    f"@{message.from_user.username}"
                    if message.from_user.username
                    else "ɴᴏ ᴜsᴇʀɴᴀᴍᴇ"
                )

                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"""
✦ {message.from_user.mention}
ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ
<b>sᴜᴅᴏʟɪsᴛ</b>.

<b>✦ ᴜsᴇʀ ɪᴅ ➜</b>
<code>{message.from_user.id}</code>

<b>✦ ᴜsᴇʀɴᴀᴍᴇ ➜</b>
{username}
""",
                    parse_mode=ParseMode.HTML,
                )

            return

        # -------------------------------------------------
        # TRACK INFO
        # -------------------------------------------------

        if name[0:3] == "inf":

            m = await message.reply_text("🔎")

            query = str(name).replace(
                "info_",
                "",
                1,
            )

            query = (
                f"https://www.youtube.com/watch?v={query}"
            )

            results = VideosSearch(
                query,
                limit=1,
            )

            data = await results.next()

            for result in data["result"]:

                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]

                thumbnail = (
                    result["thumbnails"][0]["url"]
                    .split("?")[0]
                )

                channellink = (
                    result["channel"]["link"]
                )

                channel = (
                    result["channel"]["name"]
                )

                link = result["link"]
                published = result["publishedTime"]

            searched_text = _[
                "start_6"
            ].format(
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

            try:
                await m.delete()
            except Exception:
                pass

            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )

            if await is_on_off(2):

                username = (
                    f"@{message.from_user.username}"
                    if message.from_user.username
                    else "ɴᴏ ᴜsᴇʀɴᴀᴍᴇ"
                )

                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"""
✦ {message.from_user.mention}
ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ
<b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.

✦ <b>ᴜsᴇʀ ɪᴅ ➜</b>
<code>{message.from_user.id}</code>

✦ <b>ᴜsᴇʀɴᴀᴍᴇ ➜</b>
{username}
""",
                    parse_mode=ParseMode.HTML,
                )

    # =====================================================
    # NORMAL START
    # =====================================================

    else:

        out = private_panel(_)

        await message.reply_photo(
            random.choice(shivi_PIC),
            caption=_["start_2"].format(
                message.from_user.mention,
                app.mention,
            ),
            reply_markup=InlineKeyboardMarkup(out),
        )

        if await is_on_off(2):

            username = (
                f"@{message.from_user.username}"
                if message.from_user.username
                else "ɴᴏ ᴜsᴇʀɴᴀᴍᴇ"
            )

            return await app.send_message(
                chat_id=config.LOGGER_ID,
                text=f"""
{message.from_user.mention}
ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.

<b>ᴜsᴇʀ ɪᴅ ➜</b>
<code>{message.from_user.id}</code>

<b>ᴜsᴇʀɴᴀᴍᴇ ➜</b>
{username}
""",
                parse_mode=ParseMode.HTML,
            )


# =========================================================
# GROUP /START
# =========================================================

@app.on_message(
    filters.command(["start"])
    & filters.group
    & ~BANNED_USERS
)
@LanguageStart
async def start_gp(client, message: Message, _):

    out = start_panel(_)

    uptime = int(
        time.time() - _boot_
    )

    await message.reply_photo(
        random.choice(shivi_PIC),
        caption=_["start_1"].format(
            app.mention,
            get_readable_time(uptime),
        ),
        reply_markup=InlineKeyboardMarkup(out),
    )

    return await add_served_chat(
        message.chat.id
    )


# =========================================================
# NEW CHAT MEMBER
# =========================================================

@app.on_message(
    filters.new_chat_members,
    group=-1,
)
async def welcome(client, message: Message):

    for member in message.new_chat_members:

        try:

            language = await get_lang(
                message.chat.id
            )

            _ = get_string(language)

            # -------------------------------------------------
            # BANNED USER
            # -------------------------------------------------

            if await is_banned_user(member.id):

                try:
                    await message.chat.ban_member(
                        member.id
                    )
                except Exception:
                    pass

            # -------------------------------------------------
            # BOT ADDED
            # -------------------------------------------------

            if member.id == app.id:

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

                # -------------------------------------------------
                # BLACKLISTED GROUP
                # -------------------------------------------------

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

                # -------------------------------------------------
                # GROUP WELCOME
                # -------------------------------------------------

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
                f"[ɴᴇᴡ ᴍᴇᴍʙᴇʀ ᴇʀʀᴏʀ] {ex}"
            )


# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder)
#
# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source : GitHub.com/Im-Notcoder/Purvi-V3
# 📢 Telegram : t.me/Purvi_Bots
# =======================================================
