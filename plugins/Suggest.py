from pyrogram import Client, filters
from rapidfuzz import process
from motor.motor_asyncio import AsyncIOMotorClient
from config import DATABASE_URI, DATABASE_NAME, COLLECTION_NAME

dbclient = AsyncIOMotorClient(DATABASE_URI)
db = dbclient[DATABASE_NAME][COLLECTION_NAME]

@Client.on_message(filters.command("suggest"))
async def suggest_movie(client, message):
    query = message.text.split(maxsplit=1)

    if len(query) == 1:
        return await message.reply(
            "❗ Movie ka naam likho bro.\nExample: `/suggest pathaan`"
        )

    movie_name = query[1].strip().lower()

    files = await db.find({"title": {"$exists": True}}).to_list(5000)
    movie_list = [file.get("title", "").lower() for file in files]

    if not movie_list:
        return await message.reply("❌ Database me movies nahi mili.")

    suggestions = process.extract(movie_name, movie_list, limit=5)

    if not suggestions:
        return await message.reply("❌ Koi related movies nahi mili.")

    final = "**🔍 Suggestions:**\n\n"
    for mov, score, _ in suggestions:
        final += f"🎬 {mov} — `{score}%`\n"

    await message.reply(final)