from pyrogram import Client, filters
from rapidfuzz import process
from database.users_chats_db import db

@Client.on_message(filters.private & filters.command("suggest"))
async def suggest_movies(client, message):
    query = message.text.split(maxsplit=1)
    if len(query) < 2:
        return await message.reply("❗ Movie ka naam likho bro.\nExample: `/suggest pathaan`")

    keyword = query[1].strip().lower()

    files = await db.get_all_files()
    file_names = [file.get("file_name", "") for file in files]

    if not file_names:
        return await message.reply("❌ Database me koi files nahi mila.")

    results = process.extract(keyword, file_names, limit=10)

    reply_msg = "🔍 **Top Suggestions:**\n\n"
    for movie_name, score, _ in results:
        reply_msg += f"🎬 **{movie_name}** — `{score}%`\n"

    await message.reply(reply_msg)