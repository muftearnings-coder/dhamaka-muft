#Join Telegram Channel - @TECHYUPDATEHQ

from pyrogram import Client, filters, enums
from pyrogram.types import ChatJoinRequest
from database.users_chats_db import db
from info import ADMINS, AUTH_REQ_CHANNELS
from pyrogram.filters import create

def is_auth_req_channel(_, __, update):
    return update.chat.id in AUTH_REQ_CHANNELS

@Client.on_chat_join_request(create(is_auth_req_channel))
async def join_reqs(client, message: ChatJoinRequest):
    await db.add_join_req(message.from_user.id, message.chat.id)


@Client.on_message(filters.command("delreq") & filters.private & filters.user(ADMINS))
async def del_requests(client, message):
    await db.del_join_req()    
    await message.reply("<b>⚙ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ᴄʜᴀɴɴᴇʟ ʟᴇғᴛ ᴜꜱᴇʀꜱ ᴅᴇʟᴇᴛᴇᴅ</b>")

# ==============================
# 🔥 Force Subscribe System (TechyUpdate) 🔥
# ==============================

from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os, asyncio

AUTH_CHANNELS = os.getenv("AUTH_CHANNELS")

print("🟢 Force Subscribe System Loaded:", AUTH_CHANNELS)

@Client.on_message(filters.private & filters.command("start"))
async def stylish_force_sub(client, message):
    if not AUTH_CHANNELS:
        return await message.reply_text("⚙️ AUTH_CHANNELS variable set nahi hai!")

    try:
        user = await client.get_chat_member(AUTH_CHANNELS, message.from_user.id)
        # Agar user member hai to normal welcome message
        await message.reply_text(
            f"✨ Welcome <b>{message.from_user.first_name}</b>!\n\n"
            "Aapne hamara <b>TechyUpdate</b> channel join kar liya hai ✅\n\n"
            "<b>Enjoy Premium Features 😎</b>",
            disable_web_page_preview=True
        )

    except UserNotParticipant:
        # Agar user member nahi hai to join message bhejna
        invite_link = f"https://t.me/{AUTH_CHANNELS[4:]}"  # removes '-100'
        await message.reply_photo(
            photo="https://i.ibb.co/RycJcDb/join-now.jpg",
            caption=(
                "🚨 <b>Access Denied!</b>\n\n"
                "Bot use karne ke liye pehle hamare <b>official channel</b> ko join karo 👇"
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("📢 Join TechyUpdate", url=invite_link)],
                    [InlineKeyboardButton("✅ I've Joined", callback_data="check_sub")]
                ]
            ),
        )


@Client.on_callback_query(filters.regex("check_sub"))
async def recheck_subscription(client, query):
    try:
        user = await client.get_chat_member(AUTH_CHANNELS, query.from_user.id)
        await query.message.delete()
        await query.message.reply_text(
            "✅ <b>Thank You!</b>\n\nAb aap <b>TechyUpdate Bot</b> use kar sakte ho 😎"
        )
    except UserNotParticipant:
        await query.answer("❌ Pehle channel join karo!", show_alert=True)