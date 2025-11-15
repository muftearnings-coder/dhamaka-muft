from pyrogram import Client, filters
from rapidfuzz import fuzz

MOVIES = [
    "Animal", "Gadar 2", "Pathaan", "Avatar", "KGF",
    "Pushpa", "Kantara", "Leo", "Jawan", "Salaar",
    "Tiger Zinda Hai", "Don", "Raees"
]

def best_match(query):
    best = None
    score = 0
    for name in MOVIES:
        sc = fuzz.partial_ratio(query.lower(), name.lower())
        if sc > score:
            best = name
            score = sc
    return best, score


@Client.on_message(filters.text & ~filters.command & filters.private)
async def suggest_handler(bot, msg):
    text = msg.text
    
    # skip short words
    if len(text) < 3:
        return
    
    match, score = best_match(text)
    
    if score >= 70:
        await msg.reply_text(
            f"🔍 *Did you mean:* **{match}?**\n"
            f"🤖 Confidence: {score}%\n\n"
            "👉 Type again to get movie results.",
            quote=True
        )