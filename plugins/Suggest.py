# plugins/suggest.py
# Smart Auto-Suggest (Fuzzy movie/title finder)
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import os
from rapidfuzz import fuzz, process
from motor.motor_asyncio import AsyncIOMotorClient
import time

# Config from info.py (assuming info.py exports these)
from info import DATABASE_URI, DATABASE_NAME, COLLECTION_NAME

# Settings
CACHE_REFRESH_SECONDS = int(os.getenv("SUGGEST_CACHE_REFRESH", 300))  # 5 min default
SUGGEST_LIMIT = int(os.getenv("SUGGEST_LIMIT", 5))
MIN_SCORE = int(os.getenv("SUGGEST_MIN_SCORE", 55))  # below this we may say "no good match"

# Global cache
_titles_cache = []
_cache_last_updated = 0
_cache_lock = asyncio.Lock()

# Mongo client (motor)
_mongo_client = None
_collection = None

async def init_db():
    global _mongo_client, _collection
    if _mongo_client is None:
        _mongo_client = AsyncIOMotorClient(DATABASE_URI, serverSelectionTimeoutMS=5000)
        _collection = _mongo_client[DATABASE_NAME][COLLECTION_NAME]

async def refresh_cache_if_needed():
    global _titles_cache, _cache_last_updated
    async with _cache_lock:
        now = time.time()
        if now - _cache_last_updated < CACHE_REFRESH_SECONDS and _titles_cache:
            return
        try:
            # we will fetch only needed fields to save memory (filename, title)
            cursor = _collection.find({}, {"_id": 0, "file_name": 1, "title": 1})
            titles = []
            async for doc in cursor:
                # normalize: prefer title then filename
                val = ""
                if doc.get("title"):
                    val = doc["title"]
                elif doc.get("file_name"):
                    val = doc["file_name"]
                else:
                    continue
                # keep a mapping "display text" -> original doc (for button action)
                titles.append({"text": str(val), "raw": doc})
            _titles_cache = titles
            _cache_last_updated = now
            print(f"[suggest] cache refreshed: {_cache_last_updated}, items={len(_titles_cache)}")
        except Exception as e:
            print(f"[suggest][error] cache refresh failed: {e}")

# helper: build list of strings for matching
def _build_list_for_match():
    return [t["text"] for t in _titles_cache]

# search function using rapidfuzz.process.extract
def get_suggestions(query, limit=SUGGEST_LIMIT):
    texts = _build_list_for_match()
    if not texts:
        return []
    # use token_set_ratio for fuzzy title match
    results = process.extract(query, texts, scorer=fuzz.token_set_ratio, limit=limit)
    # results -> list of tuples (matched_text, score, index)
    suggestions = []
    for matched_text, score, idx in results:
        if score < MIN_SCORE:
            continue
        item = _titles_cache[idx]
        suggestions.append({"text": matched_text, "score": score, "raw": item["raw"]})
    return suggestions

# background refresher
async def _cache_refresher_loop():
    while True:
        try:
            await refresh_cache_if_needed()
        except Exception as e:
            print(f"[suggest] refresher error: {e}")
        await asyncio.sleep(CACHE_REFRESH_SECONDS)

# start-up: called from plugin import
async def startup(app: Client):
    await init_db()
    await refresh_cache_if_needed()
    # start background refresher (daemon)
    app.loop.create_task(_cache_refresher_loop())

# Command handler
@Client.on_message(filters.command("suggest") & ~filters.edited)
async def suggest_handler(client, message):
    q = " ".join(message.command[1:]).strip() if len(message.command) > 1 else ""
    if not q:
        return await message.reply_text("❗ Usage: /suggest movie name\nFor example: /suggest john wick 4")
    # ensure cache ready
    await refresh_cache_if_needed()
    suggestions = get_suggestions(q)
    if not suggestions:
        return await message.reply_text("🔎 Koi acha result nahi mila. Thoda alag likh ke try karo.")
    # build response
    text_lines = [f"🔍 Suggestions for: <b>{q}</b>\n"]
    buttons = []
    for s in suggestions:
        score = s["score"]
        title = s["text"]
        # show score optionally
        text_lines.append(f"• <b>{title}</b>  — ({score}%)")
        # prepare button; you can change callback to trigger direct search or send file
        btn_text = title if len(title) <= 30 else (title[:27] + "...")
        # callback data can be like "suggest_select::<title>"
        buttons.append([InlineKeyboardButton(btn_text, callback_data=f"suggest_select::{title}")])
    final_text = "\n".join(text_lines)
    await message.reply_text(final_text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

# Callback handler for user clicking suggestion
@Client.on_callback_query(filters.regex(r"^suggest_select::"))
async def on_suggest_select(client, query):
    data = query.data.split("::", 1)[1]
    # you can implement what happens now: do a normal search and send first file/list
    # For now we just acknowledge and call user to do /search <title>
    await query.answer("Picked suggestion — searching...", show_alert=False)
    await query.message.edit_text(f"🔎 You selected: <b>{data}</b>\n\nUse /search {data} to fetch files.", disable_web_page_preview=True)

# ensure startup registers
# Pyrogram loads plugin file at import; if we are inside Client run, create startup hook
try:
    # this will be called when bot starts if the main script calls Client.start_plugins or import hooks.
    # But to be safe, bind to Client.on_connect by monkey patching (pyrogram has no on_connect hook by default),
    # So we export startup function — main bot file can call it after creating client.
    # If your bot's main file imports plugins automatically before start, app loop may exist already:
    pass
except Exception:
    pass