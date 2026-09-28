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


# =======================================================
# START / WELCOME PICTURES
# =======================================================

shivi_PIC = [
    "https://files.catbox.moe/4ojtc4.jpg",
    "https://files.catbox.moe/30wg78.jpg",
]


# =======================================================
# SAFE URL FUNCTION
# =======================================================

def safe_url(value, fallback=None):
    """
    Telegram InlineKeyboardButton requires a valid URL.
    This function converts @username / t.me links safely.
    """

    if not value:
        return fallback

    value = str(value).strip()

    if value.startswith("https://"):
        return value

    if value.startswith("http://"):
        return value.replace(
            "http://",
            "https://",
            1,
        )

    if value.startswith("@"):
        return f"https://t.me/{value[1:]}"

    if value.startswith("t.me/"):
        return f"https://{value}"

    return f"https://t.me/{value}"


# =======================================================
# PRIVATE GROUP JOIN REQUEST
# =======================================================
#
# User sends JOIN REQUEST
#          ↓
# Bot receives request
#          ↓
# Bot gets its own username
#          ↓
# Bot sends automatic DM
#
# =======================================================

@app.on_chat_join_request()
async def private_join_request(client, request):

    try:

        user = request.from_user
        chat = request.chat

        if not user:
            print(
                "[JOIN REQUEST] User information not found."
            )
            return

        # =================================================
        # GET CURRENT BOT
        # =================================================

        me = await client.get_me()

        bot_name = (
            me.first_name
            or "ᴍᴜsɪᴄ ʙᴏᴛ"
        )

        bot_username = me.username

        if bot_username:

            bot_display = f"@{bot_username}"

            bot_url = (
                f"https://t.me/{bot_username}"
            )

        else:

            bot_display = bot_name

            bot_url = safe_url(
                getattr(
                    config,
                    "SUPPORT_CHAT",
                    None,
                ),
                "https://t.me/",
            )

        # =================================================
        # USER / GROUP
        # =================================================

        user_name = (
            user.first_name
            or "ᴜsᴇʀ"
        )

        group_name = (
            chat.title
            or "ᴘʀɪᴠᴀᴛᴇ ɢʀᴏᴜᴘ"
        )

        # =================================================
        # UPDATE
        # =================================================

        update_url = safe_url(
            getattr(
                config,
                "UPDATE_CHAT",
                None,
            ),
            bot_url,
        )

        # =================================================
        # SUPPORT
        # =================================================

        support_url = safe_url(
            getattr(
                config,
                "SUPPORT_CHAT",
                None,
            ),
            bot_url,
        )

        # =================================================
        # ADVANCED FONT + BOLD
        # =================================================

        welcome_text = f"""
<b>ᴡᴇʟᴄᴏᴍᴇ, {user_name}!</b>

<b>ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴊᴏɪɴ {group_name} ʜᴀs ʙᴇᴇɴ ʀᴇᴄᴇɪᴠᴇᴅ.</b>

<b>ᴡʜɪʟᴇ ʏᴏᴜ ᴡᴀɪᴛ, ᴇxᴘʟᴏʀᴇ {bot_display} 🎵.</b>

<b>• ʜɪɢʜ ǫᴜᴀʟɪᴛʏ ᴍᴜsɪᴄ</b>
<b>• ғᴀsᴛ &amp; sᴍᴏᴏᴛʜ ᴘʟᴀʏʙᴀᴄᴋ</b>
<b>• sᴛᴀʙʟᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ</b>

<b>ᴜsᴇ /sᴛᴀʀᴛ ᴛᴏ ʙᴇɢɪɴ.</b>
"""

        # =================================================
        # BUTTONS
        # =================================================

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

        # =================================================
        # SEND AUTOMATIC MESSAGE
        # =================================================

        await client.send_photo(
            chat_id=request.user_chat_id,
            photo=random.choice(shivi_PIC),
            caption=welcome_text,
            parse_mode=ParseMode.HTML,
            reply_markup=buttons,
        )

        # =================================================
        # LOG
        # =================================================

        if await is_on_off(2):

            username = (
                f"@{user.username}"
                if user.username
                else "ɴᴏ ᴜsᴇʀɴᴀᴍᴇ"
            )

            logger_text = f"""
<b>✦ ɴᴇᴡ ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ</b>

<b>✦ ᴜsᴇʀ ➜</b> {user.mention}

<b>✦ ᴜsᴇʀ ɪᴅ ➜</b>
<code>{user.id}</code>

<b>✦ ᴜsᴇʀɴᴀᴍᴇ ➜</b>
{username}

<b>✦ ɢʀᴏᴜᴘ ➜</b>
{group_name}

<b>✦ ɢʀᴏᴜᴘ ɪᴅ ➜</b>
<code>{chat.id}</code>

<b>✦ ᴡᴇʟᴄᴏᴍᴇ sᴇɴᴛ ✓</b>
"""

            await client.send_message(
                chat_id=config.LOGGER_ID,
                text=logger_text,
                parse_mode=ParseMode.HTML,
            )

        print(
            f"[JOIN REQUEST] SUCCESS | "
            f"USER={user.id} | "
            f"GROUP={chat.id}"
        )

    except Exception as ex:

        print(
            f"[JOIN REQUEST] ERROR: "
            f"{type(ex).__name__}: {ex}"
        )


# =======================================================
# PRIVATE /START
# =======================================================

@app.on_message(
    filters.command("start")
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

    # ===================================================
    # START PARAMETER
    # ===================================================

    if len(message.text.split()) > 1:

        name = message.text.split(
            None,
            1,
        )[1]

        # -------------------------------------------------
        # HELP
        # -------------------------------------------------

        if name.startswith("help"):

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

        if name.startswith("sud"):

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

                await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"""
<b>✦ sᴜᴅᴏʟɪsᴛ ᴄʜᴇᴄᴋ</b>

<b>✦ ᴜsᴇʀ ➜</b>
{message.from_user.mention}

<b>✦ ᴜsᴇʀ ɪᴅ ➜</b>
<code>{message.from_user.id}</code>

<b>✦ ᴜsᴇʀɴᴀᴍᴇ ➜</b>
{username}
""",
                    parse_mode=ParseMode.HTML,
                )

            return

        # -------------------------------------------------
        # INFO
        # -------------------------------------------------

        if name.startswith("inf"):

            m = await message.reply_text(
                "🔎"
            )

            query = name.replace(
                "info_",
                "",
                1,
            )

            query = (
                "https://www.youtube.com/watch?v="
                + query
            )

            try:

                results = VideosSearch(
                    query,
                    limit=1,
                )

                data = await results.next()

                if not data.get("result"):
                    await m.edit_text(
                        "❌ ᴛʀᴀᴄᴋ ɴᴏᴛ ғᴏᴜɴᴅ."
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

                channellink = (
                    result["channel"]["link"]
                )

                channel = (
                    result["channel"]["name"]
                )

                link = result["link"]

                published = (
                    result["publishedTime"]
                )

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

                await m.delete()

                await app.send_photo(
                    chat_id=message.chat.id,
                    photo=thumbnail,
                    caption=searched_text,
                    reply_markup=key,
                )

            except Exception as ex:

                await m.edit_text(
                    f"❌ <b>ᴇʀʀᴏʀ:</b> <code>{ex}</code>",
                    parse_mode=ParseMode.HTML,
                )

            return

    # ===================================================
    # NORMAL PRIVATE START
    # ===================================================

    out = private_panel(_)

    await message.reply_photo(
        random.choice(shivi_PIC),
        caption=_["start_2"].format(
            message.from_user.mention,
            app.mention,
        ),
        reply_markup=InlineKeyboardMarkup(
            out
        ),
    )

    # ===================================================
    # LOGGER
    # ===================================================

    if await is_on_off(2):

        username = (
            f"@{message.from_user.username}"
            if message.from_user.username
            else "ɴᴏ ᴜsᴇʀɴᴀᴍᴇ"
        )

        await app.send_message(
            chat_id=config.LOGGER_ID,
            text=f"""
<b>✦ ʙᴏᴛ sᴛᴀʀᴛᴇᴅ</b>

<b>✦ ᴜsᴇʀ ➜</b>
{message.from_user.mention}

<b>✦ ᴜsᴇʀ ɪᴅ ➜</b>
<code>{message.from_user.id}</code>

<b>✦ ᴜsᴇʀɴᴀᴍᴇ ➜</b>
{username}
""",
            parse_mode=ParseMode.HTML,
        )


# =======================================================
# GROUP /START
# =======================================================

@app.on_message(
    filters.command("start")
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
        reply_markup=InlineKeyboardMarkup(
            out
        ),
    )

    await add_served_chat(
        message.chat.id
    )


# =======================================================
# BOT ADDED / NEW MEMBERS
# =======================================================

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

            # ------------------------------------------------
            # BANNED USER
            # ------------------------------------------------

            if await is_banned_user(
                member.id
            ):

                try:

                    await message.chat.ban_member(
                        member.id
                    )

                except Exception:
                    pass

            # ------------------------------------------------
            # BOT ITSELF ADDED
            # ------------------------------------------------

            if member.id == app.id:

                # --------------------------------------------
                # SUPERGROUP ONLY
                # --------------------------------------------

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

                # --------------------------------------------
                # BLACKLIST
                # --------------------------------------------

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

                # --------------------------------------------
                # GROUP WELCOME
                # --------------------------------------------

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
                f"[NEW MEMBER ERROR] {ex}"
            )


# =======================================================
# END
# =======================================================
