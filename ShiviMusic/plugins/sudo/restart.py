# ===========================================================
# ©️ 2025-26 All Rights Reserved by Kirti Bots 🚀
#
# This source code is under MIT License 📜
# ===========================================================

import asyncio
import os
import shutil
import socket
from datetime import datetime

import urllib3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from pyrogram import filters

import config
from ShiviMusic import app
from ShiviMusic.misc import HAPP, SUDOERS, XCB
from ShiviMusic.utils.database import (
    get_active_chats,
    remove_active_chat,
    remove_active_video_chat,
)
from ShiviMusic.utils.decorators.language import language
from ShiviMusic.utils.pastebin import ShiviBin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


async def is_heroku():
    return "heroku" in socket.getfqdn()


@app.on_message(
    filters.command(
        ["getlog", "logs", "getlogs"],
        prefixes=["/", "!", "%", ",", "", ".", "@", "#"],
    )
    & SUDOERS
)
@language
async def log_(client, message, _):
    try:
        await message.reply_document(document="log.txt")
    except Exception:
        await message.reply_text(_["server_1"])


@app.on_message(
    filters.command(
        ["update", "gitpull"],
        prefixes=["/", "!", "%", ",", "", ".", "@", "#"],
    )
    & SUDOERS
)
@language
async def update_(client, message, _):

    if await is_heroku():
        if HAPP is None:
            return await message.reply_text(_["server_2"])

    response = await message.reply_text(_["server_3"])

    try:
        repo = Repo()
    except GitCommandError:
        return await response.edit_text(_["server_4"])
    except InvalidGitRepositoryError:
        return await response.edit_text(_["server_5"])
    except Exception:
        return await response.edit_text(_["server_5"])

    # Fetch upstream
    to_exc = f"git fetch origin {config.UPSTREAM_BRANCH} &> /dev/null"
    os.system(to_exc)

    await asyncio.sleep(7)

    verification = ""

    try:
        REPO_ = repo.remotes.origin.url.split(".git")[0]
    except Exception:
        REPO_ = ""

    try:
        for checks in repo.iter_commits(
            f"HEAD..origin/{config.UPSTREAM_BRANCH}"
        ):
            verification = str(checks.count())
    except Exception:
        return await response.edit_text(
            "❌ Unable to check for updates."
        )

    if verification == "":
        return await response.edit_text(_["server_6"])

    updates = ""

    def ordinal(number):
        return "%d%s" % (
            number,
            "tsnrhtdd"[
                (number // 10 % 10 != 1)
                * (number % 10 < 4)
                * number % 10 :: 4
            ],
        )

    for info in repo.iter_commits(
        f"HEAD..origin/{config.UPSTREAM_BRANCH}"
    ):
        updates += (
            f"<b>➣ #{info.count()}: "
            f'<a href="{REPO_}/commit/{info}">{info.summary}</a> '
            f"ʙʏ -> {info.author}</b>\n"
            f"\t\t\t\t<b>➥ ᴄᴏᴍᴍɪᴛᴇᴅ ᴏɴ :</b> "
            f"{ordinal(int(datetime.fromtimestamp(info.committed_date).strftime('%d')))} "
            f"{datetime.fromtimestamp(info.committed_date).strftime('%b')}, "
            f"{datetime.fromtimestamp(info.committed_date).strftime('%Y')}\n\n"
        )

    _update_response_ = (
        "<b>ᴀ ɴᴇᴡ ᴜᴩᴅᴀᴛᴇ ɪs ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴛʜᴇ ʙᴏᴛ !</b>\n\n"
        "➣ ᴩᴜsʜɪɴɢ ᴜᴩᴅᴀᴛᴇs ɴᴏᴡ\n\n"
        "<b><u>ᴜᴩᴅᴀᴛᴇs:</u></b>\n\n"
    )

    _final_updates_ = _update_response_ + updates

    # Telegram message limit protection
    if len(_final_updates_) > 4096:

        url = await ShiviBin(updates)

        nrs = await response.edit_text(
            f"<b>ᴀ ɴᴇᴡ ᴜᴩᴅᴀᴛᴇ ɪs ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴛʜᴇ ʙᴏᴛ !</b>\n\n"
            f"➣ ᴩᴜsʜɪɴɢ ᴜᴩᴅᴀᴛᴇs ɴᴏᴡ\n\n"
            f"<u><b>ᴜᴩᴅᴀᴛᴇs :</b></u>\n\n"
            f'<a href="{url}">ᴄʜᴇᴄᴋ ᴜᴩᴅᴀᴛᴇs</a>'
        )

    else:

        # FIX:
        # Removed unsupported disable_web_page_preview argument.
        nrs = await response.edit_text(_final_updates_)

    # Pull latest code
    os.system("git stash &> /dev/null && git pull")

    try:
        served_chats = await get_active_chats()

        for x in served_chats:
            try:
                await app.send_message(
                    chat_id=int(x),
                    text=_["server_8"].format(app.mention),
                )

                await remove_active_chat(x)
                await remove_active_video_chat(x)

            except Exception:
                pass

        await response.edit_text(
            f"{nrs.text}\n\n{_['server_7']}"
        )

    except Exception:
        pass

    # Heroku restart
    if await is_heroku():

        try:
            os.system(
                f"{XCB[5]} {XCB[7]} {XCB[9]}"
                f"{XCB[4]}{XCB[0] * 2}{XCB[6]}{XCB[4]}"
                f"{XCB[8]}{XCB[1]}{XCB[5]}{XCB[2]}"
                f"{XCB[6]}{XCB[2]}{XCB[3]}{XCB[0]}"
                f"{XCB[10]}{XCB[2]}{XCB[5]} "
                f"{XCB[11]}{XCB[4]}{XCB[12]}"
            )
            return

        except Exception as err:

            try:
                await response.edit_text(
                    f"{nrs.text}\n\n{_['server_9']}"
                )
            except Exception:
                pass

            return await app.send_message(
                chat_id=config.LOGGER_ID,
                text=_["server_10"].format(err),
            )

    else:

        os.system("pip3 install -r requirements.txt")
        os.system(f"kill -9 {os.getpid()} && bash start")
        exit()


@app.on_message(filters.command(["restart"]) & SUDOERS)
async def restart_(_, message):

    response = await message.reply_text(
        "ʀᴇsᴛᴀʀᴛɪɴɢ..."
    )

    ac_chats = await get_active_chats()

    for x in ac_chats:
        try:

            await app.send_message(
                chat_id=int(x),
                text=(
                    f"{app.mention} ɪs ʀᴇsᴛᴀʀᴛɪɴɢ...\n\n"
                    f"ʏᴏᴜ ᴄᴀɴ sᴛᴀʀᴛ ᴩʟᴀʏɪɴɢ ᴀɢᴀɪɴ "
                    f"ᴀғᴛᴇʀ 15-20 sᴇᴄᴏɴᴅs."
                ),
            )

            await remove_active_chat(x)
            await remove_active_video_chat(x)

        except Exception:
            pass

    # Clean cache/download folders
    for folder in ["downloads", "raw_files", "cache"]:
        try:
            if os.path.exists(folder):
                shutil.rmtree(folder)
        except Exception:
            pass

    await response.edit_text(
        "» ʀᴇsᴛᴀʀᴛ ᴘʀᴏᴄᴇss sᴛᴀʀᴛᴇᴅ, "
        "ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ғᴏʀ ғᴇᴡ sᴇᴄᴏɴᴅs "
        "ᴜɴᴛɪʟ ᴛʜᴇ ʙᴏᴛ sᴛᴀʀᴛs..."
    )

    os.system(
        f"kill -9 {os.getpid()} && bash start"
    )


# ===========================================================
# ©️ 2025-26 All Rights Reserved by Kirti Bots 😎
#
# 🧑‍💻 Developer : Team Kirti Bots
# ===========================================================
