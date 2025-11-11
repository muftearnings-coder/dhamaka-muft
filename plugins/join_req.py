# Join Telegram Channel - @TECHYUPDATEHQ

from pyrogram import Client, filters, enums
from pyrogram.types import ChatJoinRequest, InlineKeyboardMarkup, InlineKeyboardButton
from database.users_chats_db import db
from info import ADMINS, AUTH_REQ_CHANNELS
from pyrogram.filters import create
from pyrogram.errors import UserNotParticipant
import os, asyncio

# =============== JOIN REQUEST SYSTEM =================
def is_auth_req_channel(_, __, update):
    return update.chat.id in AUTH_REQ_CHANNELS


@Client.on_chat_join_request(create(is_auth_req_channel))
async def join_reqs(client, message: ChatJoinRequest):
    await db.add_join_req(message.from_user.id, message.chat.id)


@Client.on_message(filters.command("delreq") & filters.private & filters.user(ADMINS))
async def del_requests(client, message):
    await db.del_join_req()
    await message.reply("<b>⚙️ Successfully deleted left users from join requests!</b>")


# ==============================
# 🔥 Force Subscribe System (TechyUpdate) 🔥
# ==============================

AUTH_CHANNELS = os.getenv("AUTH_CHANNELS")

print("🟢 Force Subscribe System Loaded:", AUTH_CHANNELS)


@Client.on_message(filters.private & filters.command("start"))
async def stylish_force_sub(client, message):
    if not AUTH_CHANNELS:
        return await message.reply_text("⚙️ AUTH_CHANNELS variable set nahi hai!")

    try:
        # ✅ Check agar user member hai
        user = await client.get_chat_member(AUTH_CHANNELS, message.from_user.id)
        await message.reply_text(
            f"✨ <b>Welcome {message.from_user.first_name}!</b>\n\n"
            "Aapne hamara <b>Official Channel</b> join kar liya hai ✅\n\n"
            "🔥 Ab aap bot ka full maza le sakte ho 😎🔥",
            disable_web_page_preview=True
        )

    except UserNotParticipant:
        # 🚫 Agar user member nahi hai to join message bhejna
        invite_link = f"https://t.me/{AUTH_CHANNELS[4:]}"  # removes '-100'
        await message.reply_photo(
            photo="https://i.ibb.co/RycJcDb/join-now.jpg",
            caption=(
                f"👋 **Hey {message.from_user.first_name}!**\n\n"
                "🚫 <b>Ruko zara, sabr rakho!</b>\n"
                "Aapne abhi tak hamara <b>Official Channel</b> join nahi kiya hai 😢\n\n"
                "👇 Pehle neeche wale button se join karo,\n"
                "fir bot ka full maza lo 😎🔥"
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("📢 Join Official Channel 📢", url=invite_link)],
                    [InlineKeyboardButton("✅ Done! I've Joined ✅", callback_data="check_sub")]
                ]
            ),
        )


@Client.on_callback_query(filters.regex("check_sub"))
async def recheck_subscription(client, query):
    try:
        user = await client.get_chat_member(AUTH_CHANNELS, query.from_user.id)
        await query.message.delete()
        await query.message.reply_text(
            f"🎉 <b>Wah {query.from_user.first_name}!</b>\n\n"
            "✅ Aapne hamara channel join kar liya hai 💖\n"
            "Ab aap bot ka poora maza le sakte ho 😎\n\n"
            "🔥 Enjoy karo aur doston ko bhi bolo — 'Bot mast hai re!' 🔥"
        )
    except UserNotParticipant:
        await query.answer("❌ Pehle channel join karo!", show_alert=True)