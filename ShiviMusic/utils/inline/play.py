import math

from pyrogram import enums
from pyrogram.types import InlineKeyboardButton

from ShiviMusic.utils.formatters import time_to_seconds


# =========================================================
# SUPPORT & UPDATE LINKS
# =========================================================

SUPPORT_URL = "https://t.me/annu_support"
UPDATE_URL = "https://t.me/annu_updates"


# =========================================================
# BUTTON STYLES
# =========================================================

PRIMARY = enums.ButtonStyle.PRIMARY
SUCCESS = enums.ButtonStyle.SUCCESS
DANGER = enums.ButtonStyle.DANGER


# =========================================================
# TRACK MARKUP
# =========================================================

def track_markup(_, videoid, user_id, channel, fplay):

    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=(
                    f"MusicStream "
                    f"{videoid}|{user_id}|a|{channel}|{fplay}"
                ),
                style=PRIMARY,
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=(
                    f"MusicStream "
                    f"{videoid}|{user_id}|v|{channel}|{fplay}"
                ),
                style=PRIMARY,
            ),
        ],
        [
            InlineKeyboardButton(
                text="Sᴜᴘᴘᴏʀᴛ",
                url=SUPPORT_URL,
                style=PRIMARY,
            ),
            InlineKeyboardButton(
                text="Uᴘᴅᴀᴛᴇ",
                url=UPDATE_URL,
                style=PRIMARY,
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=DANGER,
            ),
        ],
    ]

    return buttons


# =========================================================
# PROGRESS BAR
# =========================================================

def _progress_bar(played_sec, duration_sec):

    if not duration_sec:
        return "│●━━━━━━━━━│"

    percentage = (played_sec / duration_sec) * 100
    percentage = max(0, min(100, percentage))

    position = int(percentage // 10)

    if position <= 0:
        return "│●━━━━━━━━━│"

    if position >= 10:
        return "│━━━━━━━━━●│"

    return (
        "│"
        + "━" * position
        + "●"
        + "━" * (9 - position)
        + "│"
    )


# =========================================================
# CLOSE BUTTON
# =========================================================

def close_button():

    return [
        InlineKeyboardButton(
            text="✕ Cʟᴏsᴇ",
            callback_data="close",
            style=DANGER,
        )
    ]


# =========================================================
# STREAM MARKUP TIMER
# =========================================================

def stream_markup_timer(_, chat_id, played, dur):

    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)

    if duration_sec:
        played_sec = max(
            0,
            min(played_sec, duration_sec)
        )

    remaining_sec = max(
        0,
        duration_sec - played_sec
    )

    rem_min = remaining_sec // 60
    rem_sec = remaining_sec % 60

    remaining = f"{rem_min:02d}:{rem_sec:02d}"

    bar = _progress_bar(
        played_sec,
        duration_sec
    )

    buttons = [

        # =================================================
        # PROGRESS
        # =================================================

        [
            InlineKeyboardButton(
                text=f"{played} {bar} {remaining}",
                callback_data="bot_info_data",
                style=PRIMARY,
            )
        ],

        # =================================================
        # MAIN CONTROLS
        # =================================================

        [
            InlineKeyboardButton(
                text="▷",
                callback_data=f"ADMIN Resume|{chat_id}",
                style=SUCCESS,
            ),
            InlineKeyboardButton(
                text="Ⅱ",
                callback_data=f"ADMIN Pause|{chat_id}",
                style=PRIMARY,
            ),
            InlineKeyboardButton(
                text="↻",
                callback_data=f"ADMIN Replay|{chat_id}",
                style=PRIMARY,
            ),
            InlineKeyboardButton(
                text="▸|",
                callback_data=f"ADMIN Skip|{chat_id}",
                style=PRIMARY,
            ),
            InlineKeyboardButton(
                text="□",
                callback_data=f"ADMIN Stop|{chat_id}",
                style=DANGER,
            ),
        ],

        # =================================================
        # SEEK / RECORD
        # =================================================

        [
            InlineKeyboardButton(
                text="‹ 20ˢ",
                callback_data=f"ADMIN SeekBack|{chat_id}",
                style=PRIMARY,
            ),
            InlineKeyboardButton(
                text="🎵 REC",
                callback_data=f"ADMIN Record|{chat_id}",
                style=PRIMARY,
            ),
            InlineKeyboardButton(
                text="20ˢ ›",
                callback_data=f"ADMIN SeekFwd|{chat_id}",
                style=PRIMARY,
            ),
        ],

        # =================================================
        # FAV / AUTO
        # =================================================

        [
            InlineKeyboardButton(
                text="♥ Fᴀᴠ",
                callback_data=f"ADMIN Fav|{chat_id}",
                style=DANGER,
            ),
            InlineKeyboardButton(
                text="Aᴜᴛᴏ",
                callback_data=f"ADMIN Auto|{chat_id}",
                style=DANGER,
            ),
        ],

        # =================================================
        # CLOSE
        # =================================================

        close_button(),
    ]

    return buttons


# =========================================================
# STREAM MARKUP
# =========================================================

def stream_markup(_, chat_id):

    buttons = [

        # =================================================
        # MAIN CONTROLS
        # =================================================

        [
            InlineKeyboardButton(
                text="▷",
                callback_data=f"ADMIN Resume|{chat_id}",
                style=SUCCESS,
            ),
            InlineKeyboardButton(
                text="Ⅱ",
                callback_data=f"ADMIN Pause|{chat_id}",
                style=PRIMARY,
            ),
            InlineKeyboardButton(
                text="↻",
                callback_data=f"ADMIN Replay|{chat_id}",
                style=PRIMARY,
            ),
            InlineKeyboardButton(
                text="▸|",
                callback_data=f"ADMIN Skip|{chat_id}",
                style=PRIMARY,
            ),
            InlineKeyboardButton(
                text="□",
                callback_data=f"ADMIN Stop|{chat_id}",
                style=DANGER,
            ),
        ],

        # =================================================
        # SEEK / RECORD
        # =================================================

        [
            InlineKeyboardButton(
                text="‹ 20ˢ",
                callback_data=f"ADMIN SeekBack|{chat_id}",
                style=PRIMARY,
            ),
            InlineKeyboardButton(
                text="🎵 REC",
                callback_data=f"ADMIN Record|{chat_id}",
                style=PRIMARY,
            ),
            InlineKeyboardButton(
                text="20ˢ ›",
                callback_data=f"ADMIN SeekFwd|{chat_id}",
                style=PRIMARY,
            ),
        ],

        # =================================================
        # FAV / AUTO
        # =================================================

        [
            InlineKeyboardButton(
                text="♥ Fᴀᴠ",
                callback_data=f"ADMIN Fav|{chat_id}",
                style=DANGER,
            ),
            InlineKeyboardButton(
                text="Aᴜᴛᴏ",
                callback_data=f"ADMIN Auto|{chat_id}",
                style=DANGER,
            ),
        ],

        # =================================================
        # CLOSE
        # =================================================

        close_button(),
    ]

    return buttons


# =========================================================
# PLAYLIST MARKUP
# =========================================================

def playlist_markup(
    _,
    videoid,
    user_id,
    ptype,
    channel,
    fplay,
):

    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=(
                    f"ShiviPlaylists "
                    f"{videoid}|{user_id}|{ptype}|a|{channel}|{fplay}"
                ),
                style=PRIMARY,
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=(
                    f"ShiviPlaylists "
                    f"{videoid}|{user_id}|{ptype}|v|{channel}|{fplay}"
                ),
                style=PRIMARY,
            ),
        ],
        [
            InlineKeyboardButton(
                text="Sᴜᴘᴘᴏʀᴛ",
                url=SUPPORT_URL,
                style=PRIMARY,
            ),
            InlineKeyboardButton(
                text="Uᴘᴅᴀᴛᴇ",
                url=UPDATE_URL,
                style=PRIMARY,
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=DANGER,
            ),
        ],
    ]

    return buttons


# =========================================================
# LIVESTREAM MARKUP
# =========================================================

def livestream_markup(
    _,
    videoid,
    user_id,
    mode,
    channel,
    fplay,
):

    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=(
                    f"LiveStream "
                    f"{videoid}|{user_id}|{mode}|{channel}|{fplay}"
                ),
                style=PRIMARY,
            ),
        ],
        [
            InlineKeyboardButton(
                text="Sᴜᴘᴘᴏʀᴛ",
                url=SUPPORT_URL,
                style=PRIMARY,
            ),
            InlineKeyboardButton(
                text="Uᴘᴅᴀᴛᴇ",
                url=UPDATE_URL,
                style=PRIMARY,
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=DANGER,
            ),
        ],
    ]

    return buttons


# =========================================================
# SLIDER MARKUP
# =========================================================

def slider_markup(
    _,
    videoid,
    user_id,
    query,
    query_type,
    channel,
    fplay,
):

    query = query[:20]

    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=(
                    f"MusicStream "
                    f"{videoid}|{user_id}|a|{channel}|{fplay}"
                ),
                style=PRIMARY,
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=(
                    f"MusicStream "
                    f"{videoid}|{user_id}|v|{channel}|{fplay}"
                ),
                style=PRIMARY,
            ),
        ],
        [
            InlineKeyboardButton(
                text="◁",
                callback_data=(
                    f"slider B|{query_type}|{query}|"
                    f"{user_id}|{channel}|{fplay}"
                ),
                style=PRIMARY,
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {query}|{user_id}",
                style=DANGER,
            ),
            InlineKeyboardButton(
                text="▷",
                callback_data=(
                    f"slider F|{query_type}|{query}|"
                    f"{user_id}|{channel}|{fplay}"
                ),
                style=PRIMARY,
            ),
        ],
        [
            InlineKeyboardButton(
                text="Sᴜᴘᴘᴏʀᴛ",
                url=SUPPORT_URL,
                style=PRIMARY,
            ),
            InlineKeyboardButton(
                text="Uᴘᴅᴀᴛᴇ",
                url=UPDATE_URL,
                style=PRIMARY,
            ),
        ],
    ]

    return buttons
