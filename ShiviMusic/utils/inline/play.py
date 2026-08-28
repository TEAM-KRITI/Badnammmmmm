# ======================================================
# ©️ 2025-26 All Rights Reserved by Kirti 😎
# 🧑‍💻 Developer : t.me/lll_APNA_BADNAM_BABY_lll
# ======================================================

import math
import random

from pyrogram.types import InlineKeyboardButton
from pyrogram.enums import ButtonStyle

from ShiviMusic import app
from ShiviMusic.utils.formatters import time_to_seconds


styles = [
    ButtonStyle.PRIMARY,
    ButtonStyle.SUCCESS,
    ButtonStyle.DANGER,
]


# ======================================================
# TRACK MARKUP
# ======================================================

def track_markup(_, videoid, user_id, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=(
                    f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}"
                ),
                style=random.choice(styles),
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=(
                    f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}"
                ),
                style=random.choice(styles),
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=random.choice(styles),
            )
        ],
    ]


# ======================================================
# FIXED PROGRESS BAR
# ======================================================

def progress_bar(played, dur):
    try:
        played_sec = time_to_seconds(str(played))
        duration_sec = time_to_seconds(str(dur))

        played_sec = max(0, int(played_sec))
        duration_sec = max(0, int(duration_sec))

        if duration_sec <= 0:
            return "●────────────────────"

        # Prevent progress from going above duration
        played_sec = min(played_sec, duration_sec)

        # Calculate percentage
        percentage = played_sec / duration_sec

        # 21 characters
        total_blocks = 21

        position = int(
            percentage * (total_blocks - 1)
        )

        position = max(
            0,
            min(position, total_blocks - 1)
        )

        bar = ["─"] * total_blocks
        bar[position] = "●"

        return "".join(bar)

    except Exception:
        return "●────────────────────"


# ======================================================
# ADMIN BUTTONS
# ======================================================

def admin_buttons(chat_id):
    return [
        [
            InlineKeyboardButton(
                "▷",
                callback_data=f"ADMIN Resume|{chat_id}",
                style=random.choice(styles),
            ),
            InlineKeyboardButton(
                "II",
                callback_data=f"ADMIN Pause|{chat_id}",
                style=random.choice(styles),
            ),
            InlineKeyboardButton(
                "↻",
                callback_data=f"ADMIN Replay|{chat_id}",
                style=random.choice(styles),
            ),
            InlineKeyboardButton(
                "‣‣I",
                callback_data=f"ADMIN Skip|{chat_id}",
                style=random.choice(styles),
            ),
            InlineKeyboardButton(
                "▢",
                callback_data=f"ADMIN Stop|{chat_id}",
                style=random.choice(styles),
            ),
        ],
        [
            InlineKeyboardButton(
                "< - 𝟤𝟢ˢ",
                callback_data="seek_backward_20",
                style=random.choice(styles),
            ),
            InlineKeyboardButton(
                "🔂",
                callback_data=f"ADMIN Loop|{chat_id}",
                style=random.choice(styles),
            ),
            InlineKeyboardButton(
                "🔁",
                callback_data=f"ADMIN AutoPlay|{chat_id}",
                style=random.choice(styles),
            ),
            InlineKeyboardButton(
                "𝟤𝟢ˢ + >",
                callback_data="seek_forward_20",
                style=random.choice(styles),
            ),
        ],
    ]


# ======================================================
# STREAM TIMER MARKUP
# ======================================================

def stream_markup_timer(_, chat_id, played, dur):
    try:
        played = str(played)
        dur = str(dur)

        bar = progress_bar(
            played,
            dur
        )

        return [
            [
                InlineKeyboardButton(
                    f"{played}  {bar}  {dur}",
                    callback_data="GetTimer",
                    style=random.choice(styles),
                )
            ],

            *admin_buttons(chat_id),

            [
                InlineKeyboardButton(
                    "✙ ʌᴅᴅ ϻє ✙",
                    url=(
                        f"https://t.me/"
                        f"{app.username}"
                        f"?startgroup=true"
                    ),
                    style=random.choice(styles),
                ),
                InlineKeyboardButton(
                    _["CLOSE_BUTTON"],
                    callback_data="close",
                    style=random.choice(styles),
                ),
            ],
        ]

    except Exception:
        return stream_markup(_, chat_id)


# ======================================================
# NORMAL STREAM MARKUP
# ======================================================

def stream_markup(_, chat_id):
    return [
        *admin_buttons(chat_id),

        [
            InlineKeyboardButton(
                "✙ ʌᴅᴅ ϻє ✙",
                url=(
                    f"https://t.me/"
                    f"{app.username}"
                    f"?startgroup=true"
                ),
                style=random.choice(styles),
            ),
            InlineKeyboardButton(
                _["CLOSE_BUTTON"],
                callback_data="close",
                style=random.choice(styles),
            ),
        ],
    ]


# ======================================================
# PLAYLIST MARKUP
# ======================================================

def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=(
                    f"ShiviPlaylists "
                    f"{videoid}|{user_id}|{ptype}|a|{channel}|{fplay}"
                ),
                style=random.choice(styles),
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=(
                    f"ShiviPlaylists "
                    f"{videoid}|{user_id}|{ptype}|v|{channel}|{fplay}"
                ),
                style=random.choice(styles),
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=random.choice(styles),
            )
        ],
    ]


# ======================================================
# LIVE STREAM MARKUP
# ======================================================

def livestream_markup(
    _,
    videoid,
    user_id,
    mode,
    channel,
    fplay
):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=(
                    f"LiveStream "
                    f"{videoid}|{user_id}|{mode}|{channel}|{fplay}"
                ),
                style=random.choice(styles),
            )
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=random.choice(styles),
            )
        ],
    ]


# ======================================================
# SLIDER MARKUP
# ======================================================

def slider_markup(
    _,
    videoid,
    user_id,
    query,
    query_type,
    channel,
    fplay
):
    query = str(query)[:20]

    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=(
                    f"MusicStream "
                    f"{videoid}|{user_id}|a|{channel}|{fplay}"
                ),
                style=random.choice(styles),
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=(
                    f"MusicStream "
                    f"{videoid}|{user_id}|v|{channel}|{fplay}"
                ),
                style=random.choice(styles),
            ),
        ],
        [
            InlineKeyboardButton(
                "◁",
                callback_data=(
                    f"slider B|"
                    f"{query_type}|"
                    f"{query}|"
                    f"{user_id}|"
                    f"{channel}|"
                    f"{fplay}"
                ),
                style=random.choice(styles),
            ),
            InlineKeyboardButton(
                _["CLOSE_BUTTON"],
                callback_data=f"forceclose {query}|{user_id}",
                style=random.choice(styles),
            ),
            InlineKeyboardButton(
                "▷",
                callback_data=(
                    f"slider F|"
                    f"{query_type}|"
                    f"{query}|"
                    f"{user_id}|"
                    f"{channel}|"
                    f"{fplay}"
                ),
                style=random.choice(styles),
            ),
        ],
    ]
