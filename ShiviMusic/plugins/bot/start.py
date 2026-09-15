# =======================================================
# ©️ 2025-26 All Rights Reserved by kirti Bots
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
from ShiviMusic.misc import boot
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

=======================================================

🖼️ START PHOTOS

=======================================================

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

=======================================================

📩 PRIVATE /START

=======================================================

@app.on_message(
filters.command(["start"])
& filters.private
& ~BANNED_USERS
)
@LanguageStart
async def start_pm(client, message: Message, _):

await add_served_user(message.from_user.id)  

try:  
    await message.delete()  
except Exception:  
    pass  

# ===================================================  
# START WITH ARGUMENT  
# ===================================================  

if len(message.text.split()) > 1:  

    name = message.text.split(None, 1)[1]  

    # ------------------------------------------------  
    # HELP  
    # ------------------------------------------------  

    if name[0:4] == "help":  

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

    if name[0:3] == "sud":  

        await sudoers_list(  
            client=client,  
            message=message,  
            _=_,  
        )  

        if await is_on_off(2):  

            return await app.send_message(  
                chat_id=config.LOGGER_ID,  
                text=(  
                    f"✦ {message.from_user.mention} "  
                    f"ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ "  
                    f"<b>sᴜᴅᴏʟɪsᴛ</b>.\n\n"  
                    f"<b>✦ ᴜsᴇʀ ɪᴅ ➠</b> "  
                    f"<code>{message.from_user.id}</code>\n"  
                    f"<b>✦ ᴜsᴇʀɴᴀᴍᴇ ➠</b> "  
                    f"@{message.from_user.username}"  
                ),  
            )  

        return  

    # ------------------------------------------------  
    # YOUTUBE INFO  
    # ------------------------------------------------  

    if name[0:3] == "inf":  

        m = await message.reply_text("🔎")  

        query = name.replace(  
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
                    f"✦ {message.from_user.mention} "  
                    f"ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ "  
                    f"ᴛᴏ ᴄʜᴇᴄᴋ "  
                    f"<b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n"  
                    f"✦ <b>ᴜsᴇʀ ɪᴅ ➠</b> "  
                    f"<code>{message.from_user.id}</code>\n"  
                    f"✦ <b>ᴜsᴇʀɴᴀᴍᴇ ➠</b> "  
                    f"@{message.from_user.username}"  
                ),  
            )  

# ===================================================  
# NORMAL PRIVATE START  
# ===================================================  

else:  

    out = private_panel(_)  

    await message.reply_photo(  
        random.choice(shivi_PIC),  
        has_spoiler=True,  
        caption=_["start_2"].format(  
            message.from_user.mention,  
            app.mention,  
        ),  
        reply_markup=InlineKeyboardMarkup(out),  
    )  

    if await is_on_off(2):  

        return await app.send_message(  
            chat_id=config.LOGGER_ID,  
            text=(  
                f"{message.from_user.mention} "  
                f"ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n"  
                f"<b>ᴜsᴇʀ ɪᴅ :</b> "  
                f"<code>{message.from_user.id}</code>\n"  
                f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> "  
                f"@{message.from_user.username}"  
            ),  
        )

=======================================================

📩 JOIN REQUEST → PRIVATE WELCOME

=======================================================

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

    # Telegram temporary user chat ID  
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
    # ✨ PREMIUM WELCOME MESSAGE  
    # =================================================  

    caption = (  
        f"<b>🌸 ᴡᴇʟᴄᴏᴍᴇ, {user.mention} 🇮🇳</b>\n\n"  

        f"✨ ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴊᴏɪɴ "  
        f"<b>{group_title}</b> "  
        f"ʜᴀs ʙᴇᴇɴ ʀᴇᴄᴇɪᴠᴇᴅ. ✅\n\n"  

        f"💎 <b>ᴛʜᴀɴᴋ ʏᴏᴜ ғᴏʀ ᴄʜᴏᴏsɪɴɢ "  
        f"{app.mention}</b>\n\n"  

        f"🎶 ᴇɴᴊᴏʏ ʜɪɢʜ-ǫᴜᴀʟɪᴛʏ ᴍᴜsɪᴄ ᴡɪᴛʜ "  
        f"{app.mention}. ✨\n\n"  

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
    # 📤 SEND PRIVATE WELCOME  
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

=======================================================

👥 GROUP /START

=======================================================

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

=======================================================

👋 NEW MEMBER WELCOME

=======================================================

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

            # Bot cannot work in normal group  
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
            # BLACKLISTED CHAT  
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
            # NORMAL BOT WELCOME  
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

        print(ex)

=======================================================

©️ 2025-26 All Rights Reserved by kirti Bots

=======================================================

