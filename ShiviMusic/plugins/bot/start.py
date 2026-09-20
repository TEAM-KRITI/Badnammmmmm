# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder)
# Modified UI / Start Flow
# =======================================================

import time
import random
from html import escape

from pyrogram import filters
from pyrogram.enums import ChatType
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
# START IMAGES
# =======================================================

shivi_PIC = [
    "https://d.uguu.se/AHWUtCcF.jpg",
    "https://h.uguu.se/oCKonQPF.jpg",
    "https://o.uguu.se/ZKmYOtBA.jpg",
    "https://d.uguu.se/CPlUJSEp.jpg",
    "https://h.uguu.se/LSyRfkrb.jpg",
    "https://h.uguu.se/ALtehGVn.jpg",
    "https://d.uguu.se/TOCZFbxQ.jpg",
]


# =======================================================
# CONFIG HELPERS
# =======================================================

UPDATE_CHANNEL = getattr(
    config,
    "UPDATE_CHANNEL",
    config.SUPPORT_CHAT,
)

SUPPORT_CHAT = getattr(
    config,
    "SUPPORT_CHAT",
    "https://t.me/",
)


# =======================================================
# CLEAN DM WELCOME TEXT
# =======================================================

def make_dm_text(user, group_name=None):
    user_name = user.mention

    group_line = ""

    if group_name:
        group_line = (
            f"\n"
            f"✦ ɢʀᴏᴜᴘ: <b>{escape(group_name)}</b>\n"
        )

    return f"""
✦ ᴡᴇʟᴄᴏᴍᴇ, {user_name} 🇮🇳

ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ʜᴀs ʙᴇᴇɴ ʀᴇᴄᴇɪᴠᴇᴅ. ✅
{group_line}
ᴡʜɪʟᴇ ʏᴏᴜ ᴡᴀɪᴛ, ᴇxᴘʟᴏʀᴇ ᴏᴜʀ ʙᴏᴛ 💗

• ʜɪɢʜ ǫᴜᴀʟɪᴛʏ ᴍᴜsɪᴄ
• ғᴀsᴛ & sᴍᴏᴏᴛʜ ᴘʟᴀʏʙᴀᴄᴋ
• sᴛᴀʙʟᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ

ᴜsᴇ /sᴛᴀʀᴛ ᴛᴏ ʙᴇɢɪɴ.
"""


# =======================================================
# DM BUTTONS
# =======================================================

def dm_buttons():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "≡ ᴍᴏʀᴇ ɪɴғᴏ ≡",
                    callback_data="help_callback",
                )
            ],
            [
                InlineKeyboardButton(
                    "≡ ᴜᴘᴅᴀᴛᴇs ≡",
                    url=UPDATE_CHANNEL,
                ),
                InlineKeyboardButton(
                    "≡ sᴜᴘᴘᴏʀᴛ ≡",
                    url=SUPPORT_CHAT,
                ),
            ],
        ]
    )


# =======================================================
# PRIVATE /start
# =======================================================

@app.on_message(
    filters.command(["start"])
    & filters.private
    & ~BANNED_USERS
)
@LanguageStart
async def start_pm(client, message: Message, _):

    user_id = message.from_user.id

    # ---------------------------------------------------
    # SAVE USER
    # ---------------------------------------------------

    try:
        await add_served_user(user_id)
    except Exception as ex:
        print(f"add_served_user error: {ex}")

    # ---------------------------------------------------
    # DELETE /start COMMAND
    # ---------------------------------------------------

    try:
        await message.delete()
    except Exception:
        pass

    # ---------------------------------------------------
    # GET START PAYLOAD
    # ---------------------------------------------------

    payload = None

    try:
        parts = message.text.split(maxsplit=1)

        if len(parts) > 1:
            payload = parts[1].strip()
    except Exception:
        payload = None

    # ===================================================
    # HELP
    # ===================================================

    if payload and payload.startswith("help"):

        keyboard = help_pannel(_)

        return await message.reply_photo(
            photo=random.choice(shivi_PIC),
            caption=_["help_1"].format(config.SUPPORT_CHAT),
            reply_markup=keyboard,
        )

    # ===================================================
    # SUDO LIST
    # ===================================================

    if payload and payload.startswith("sud"):

        await sudoers_list(
            client=client,
            message=message,
            _=_,
        )

        if await is_on_off(2):

            try:
                await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=(
                        f"✦ {message.from_user.mention} "
                        f"ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ "
                        f"<b>sᴜᴅᴏʟɪsᴛ</b>.\n\n"

                        f"<b>✦ ᴜsᴇʀ ɪᴅ ➠</b> "
                        f"<code>{user_id}</code>\n"

                        f"<b>✦ ᴜsᴇʀɴᴀᴍᴇ ➠</b> "
                        f"@{message.from_user.username or 'None'}"
                    ),
                )
            except Exception as ex:
                print(f"Logger error: {ex}")

        return

    # ===================================================
    # TRACK INFO
    # ===================================================

    if payload and payload.startswith("inf"):

        m = await message.reply_text("🔎")

        try:

            query = payload.replace(
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

            result_list = data.get("result", [])

            if not result_list:
                await m.edit_text(
                    "❌ ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ɴᴏᴛ ғᴏᴜɴᴅ."
                )
                return

            result = result_list[0]

            title = result.get(
                "title",
                "Unknown",
            )

            duration = result.get(
                "duration",
                "Unknown",
            )

            views = result.get(
                "viewCount",
                {},
            ).get(
                "short",
                "Unknown",
            )

            thumbnails = result.get(
                "thumbnails",
                [],
            )

            thumbnail = (
                thumbnails[0]["url"].split("?")[0]
                if thumbnails
                else random.choice(shivi_PIC)
            )

            channel_data = result.get(
                "channel",
                {},
            )

            channellink = channel_data.get(
                "link",
                "",
            )

            channel = channel_data.get(
                "name",
                "Unknown",
            )

            link = result.get(
                "link",
                "",
            )

            published = result.get(
                "publishedTime",
                "Unknown",
            )

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
                    ]
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

                try:
                    await app.send_message(
                        chat_id=config.LOGGER_ID,
                        text=(
                            f"✦ {message.from_user.mention} "
                            f"ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ "
                            f"<b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n"

                            f"✦ <b>ᴜsᴇʀ ɪᴅ ➠</b> "
                            f"<code>{user_id}</code>\n"

                            f"✦ <b>ᴜsᴇʀɴᴀᴍᴇ ➠</b> "
                            f"@{message.from_user.username or 'None'}"
                        ),
                    )
                except Exception as ex:
                    print(f"Logger error: {ex}")

            return

        except Exception as ex:

            print(f"Track info error: {ex}")

            try:
                await m.edit_text(
                    "❌ ᴜɴᴀʙʟᴇ ᴛᴏ ғᴇᴛᴄʜ ᴛʀᴀᴄᴋ ɪɴғᴏ."
                )
            except Exception:
                pass

            return

    # ===================================================
    # GROUP PAYLOAD
    #
    # /start group_-100123456789
    # ===================================================

    group_name = None

    if payload and payload.startswith("group_"):

        group_id_text = payload.replace(
            "group_",
            "",
            1,
        )

        try:

            group_id = int(group_id_text)

            group_chat = await app.get_chat(
                group_id
            )

            group_name = group_chat.title

        except Exception as ex:

            print(
                f"Unable to get group information: {ex}"
            )

            group_name = None

    # ===================================================
    # NORMAL DM START
    # ===================================================

    text = make_dm_text(
        message.from_user,
        group_name,
    )

    await message.reply_photo(
        photo=random.choice(shivi_PIC),
        caption=text,
        reply_markup=dm_buttons(),
    )

    # ===================================================
    # LOGGER
    # ===================================================

    if await is_on_off(2):

        try:

            group_log = (
                f"\n<b>ɢʀᴏᴜᴘ :</b> "
                f"<code>{escape(group_name)}</code>"
                if group_name
                else ""
            )

            await app.send_message(
                chat_id=config.LOGGER_ID,
                text=(
                    f"✦ {message.from_user.mention} "
                    f"ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n"

                    f"<b>ᴜsᴇʀ ɪᴅ :</b> "
                    f"<code>{user_id}</code>\n"

                    f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> "
                    f"@{message.from_user.username or 'None'}"
                    f"{group_log}"
                ),
            )

        except Exception as ex:

            print(
                f"Start logger error: {ex}"
            )


# =======================================================
# GROUP /start
# =======================================================

@app.on_message(
    filters.command(["start"])
    & filters.group
    & ~BANNED_USERS
)
@LanguageStart
async def start_gp(client, message: Message, _):

    try:

        out = start_panel(_)

        uptime = int(
            time.time() - _boot_
        )

        await message.reply_photo(
            photo=random.choice(shivi_PIC),
            caption=_["start_1"].format(
                app.mention,
                get_readable_time(uptime),
            ),
            reply_markup=InlineKeyboardMarkup(out),
        )

        await add_served_chat(
            message.chat.id
        )

    except Exception as ex:

        print(
            f"Group start error: {ex}"
        )


# =======================================================
# BOT ADDED TO GROUP
# =======================================================

@app.on_message(
    filters.new_chat_members,
    group=-1,
)
async def welcome(client, message: Message):

    try:

        # ------------------------------------------------
        # CHECK WHETHER OUR BOT JOINED
        # ------------------------------------------------

        bot_joined = any(
            member.id == app.id
            for member in message.new_chat_members
        )

        if not bot_joined:
            return

        # ------------------------------------------------
        # LANGUAGE
        # ------------------------------------------------

        language = await get_lang(
            message.chat.id
        )

        _ = get_string(
            language
        )

        # ------------------------------------------------
        # BAN CHECK FOR USERS
        # ------------------------------------------------

        for member in message.new_chat_members:

            try:

                if await is_banned_user(
                    member.id
                ):

                    try:
                        await message.chat.ban_member(
                            member.id
                        )
                    except Exception:
                        pass

            except Exception:
                pass

        # ------------------------------------------------
        # ONLY SUPERGROUP
        # ------------------------------------------------

        if message.chat.type != ChatType.SUPERGROUP:

            try:
                await message.reply_text(
                    _["start_4"]
                )
            except Exception:
                pass

            return await app.leave_chat(
                message.chat.id
            )

        # ------------------------------------------------
        # BLACKLIST
        # ------------------------------------------------

        if message.chat.id in await blacklisted_chats():

            try:

                await message.reply_text(
                    _["start_5"].format(
                        app.mention,
                        f"https://t.me/"
                        f"{app.username}"
                        f"?start=sudolist",
                        config.SUPPORT_CHAT,
                    ),
                    disable_web_page_preview=True,
                )

            except Exception:
                pass

            return await app.leave_chat(
                message.chat.id
            )

        # ------------------------------------------------
        # SAVE GROUP
        # ------------------------------------------------

        await add_served_chat(
            message.chat.id
        )

        # ------------------------------------------------
        # GROUP NAME
        # ------------------------------------------------

        group_name = (
            message.chat.title
            or "Unknown Group"
        )

        safe_group_name = escape(
            group_name
        )

        # ------------------------------------------------
        # ADDER / USER WHO ADDED BOT
        # ------------------------------------------------

        adder = message.from_user

        # ------------------------------------------------
        # DEEP LINK
        #
        # User clicks this button -> DM opens with:
        # /start group_<group_id>
        # ------------------------------------------------

        start_link = (
            f"https://t.me/"
            f"{app.username}"
            f"?start=group_{message.chat.id}"
        )

        # ------------------------------------------------
        # GROUP BUTTONS
        # ------------------------------------------------

        group_buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✦ ᴏᴘᴇɴ ᴅᴍ ✦",
                        url=start_link,
                    )
                ],
                [
                    InlineKeyboardButton(
                        "≡ ᴜᴘᴅᴀᴛᴇs ≡",
                        url=UPDATE_CHANNEL,
                    ),
                    InlineKeyboardButton(
                        "≡ sᴜᴘᴘᴏʀᴛ ≡",
                        url=SUPPORT_CHAT,
                    ),
                ],
            ]
        )

        # ------------------------------------------------
        # GROUP WELCOME
        # ------------------------------------------------

        group_text = f"""
✦ ʙᴏᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ 🇮🇳

✦ ɢʀᴏᴜᴘ: <b>{safe_group_name}</b>

ʜᴇʟʟᴏ {adder.mention if adder else "Admin"} 💗

ᴛʜᴀɴᴋ ʏᴏᴜ ғᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ᴛᴏ
<b>{safe_group_name}</b>. ✅

• ʜɪɢʜ ǫᴜᴀʟɪᴛʏ ᴍᴜsɪᴄ
• ғᴀsᴛ & sᴍᴏᴏᴛʜ ᴘʟᴀʏʙᴀᴄᴋ
• sᴛᴀʙʟᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ

ᴜsᴇ /sᴛᴀʀᴛ ᴛᴏ ʙᴇɢɪɴ.
"""

        # ------------------------------------------------
        # SEND GROUP MESSAGE
        # ------------------------------------------------

        await message.reply_text(
            text=group_text,
            reply_markup=group_buttons,
            disable_web_page_preview=True,
        )

        # =================================================
        # TRY TO SEND DM TO PERSON WHO ADDED BOT
        # =================================================

        if adder:

            try:

                await add_served_user(
                    adder.id
                )

                dm_text = make_dm_text(
                    adder,
                    group_name,
                )

                dm_buttons_markup = dm_buttons()

                await app.send_photo(
                    chat_id=adder.id,
                    photo=random.choice(
                        shivi_PIC
                    ),
                    caption=dm_text,
                    reply_markup=dm_buttons_markup,
                )

            except Exception as dm_error:

                # User has not started the bot yet
                print(
                    f"DM send failed: {dm_error}"
                )

        # ------------------------------------------------
        # LOGGER
        # ------------------------------------------------

        if await is_on_off(2):

            try:

                username = (
                    f"@{adder.username}"
                    if adder and adder.username
                    else "None"
                )

                adder_id = (
                    adder.id
                    if adder
                    else "Unknown"
                )

                await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=(
                        f"✦ <b>ʙᴏᴛ ᴀᴅᴅᴇᴅ ᴛᴏ ɢʀᴏᴜᴘ</b>\n\n"

                        f"✦ <b>ɢʀᴏᴜᴘ ɴᴀᴍᴇ :</b> "
                        f"<code>{safe_group_name}</code>\n"

                        f"✦ <b>ɢʀᴏᴜᴘ ɪᴅ :</b> "
                        f"<code>{message.chat.id}</code>\n\n"

                        f"✦ <b>ᴀᴅᴅᴇᴅ ʙʏ :</b> "
                        f"{adder.mention if adder else 'Unknown'}\n"

                        f"✦ <b>ᴜsᴇʀ ɪᴅ :</b> "
                        f"<code>{adder_id}</code>\n"

                        f"✦ <b>ᴜsᴇʀɴᴀᴍᴇ :</b> "
                        f"{username}"
                    ),
                )

            except Exception as log_error:

                print(
                    f"Join logger error: {log_error}"
                )

        # ------------------------------------------------
        # STOP PROPAGATION
        # ------------------------------------------------

        await message.stop_propagation()

    except Exception as ex:

        print(
            f"Bot Join Error: {ex}"
        )


# =======================================================
# MORE INFO BUTTON
# =======================================================

@app.on_callback_query(
    filters.regex("^help_callback$")
)
async def more_info_callback(client, callback_query):

    try:

        language = await get_lang(
            callback_query.message.chat.id
        )

        _ = get_string(
            language
        )

        keyboard = help_pannel(_)

        await callback_query.message.edit_reply_markup(
            reply_markup=keyboard
        )

        await callback_query.answer(
            "✦ ᴏᴘᴇɴɪɴɢ ᴍᴏʀᴇ ɪɴғᴏ...",
            show_alert=False,
        )

    except Exception as ex:

        print(
            f"Help callback error: {ex}"
        )

        try:
            await callback_query.answer(
                "❌ ᴜɴᴀʙʟᴇ ᴛᴏ ᴏᴘᴇɴ ᴍᴏʀᴇ ɪɴғᴏ.",
                show_alert=True,
            )
        except Exception:
            pass


# =======================================================
# ©️ 2025-26
# =======================================================
