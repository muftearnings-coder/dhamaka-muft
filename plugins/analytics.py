from pyrogram import Client, filters
from datetime import datetime, timedelta
from database.users_chats_db import db
from info import ADMINS, PREMIUM_USER


def bar(percent):
    filled = int(percent / 10)
    return "█" * filled + "░" * (10 - filled)


@Client.on_message(filters.command("analytics") & filters.user(ADMINS))
async def full_analytics(client, message):

    users = await db.get_all_users()
    total_users = await db.total_users_count()

    now = datetime.now()

    today_users = 0
    last_24h = 0
    last_7d = 0
    last_30d = 0

    hourly_count = [0] * 24

    async for user in users:
        try:
            join_time = datetime.fromtimestamp(int(user["date"]))
        except:
            continue

        if join_time.date() == now.date():
            today_users += 1
            hourly_count[join_time.hour] += 1

        if now - timedelta(hours=24) <= join_time:
            last_24h += 1

        if now - timedelta(days=7) <= join_time:
            last_7d += 1

        if now - timedelta(days=30) <= join_time:
            last_30d += 1

    premium_count = len(PREMIUM_USER)

    # Weekly Chart
    last_7_counts = {}
    async for user in users:
        try:
            join_time = datetime.fromtimestamp(int(user["date"]))
        except:
            continue

        day = join_time.strftime("%a")
        if now - timedelta(days=7) <= join_time:
            last_7_counts[day] = last_7_counts.get(day, 0) + 1

    week_chart = ""
    for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
        c = last_7_counts.get(day, 0)
        week_chart += f"{day}: {bar(min(100, c))} ({c})\n"

    # Hourly chart
    hourly_graph = ""
    for hr in range(24):
        hourly_graph += f"{hr:02d}:00 → {bar(min(100, hourly_count[hr]))} ({hourly_count[hr]})\n"

    text = f"""
📊 <b>FULL USER ANALYTICS</b>

👥 <b>Total Users:</b> {total_users}
🆕 <b>Today Users:</b> {today_users}
⏳ <b>Last 24 Hours:</b> {last_24h}
📅 <b>Last 7 Days:</b> {last_7d}
📆 <b>Last 30 Days:</b> {last_30d}

⭐ <b>Premium Users:</b> {premium_count}

────────────────────
📈 <b>Today - Hourly Analytics</b>
{hourly_graph}

────────────────────
📆 <b>Weekly Join Chart</b>
{week_chart}

────────────────────
🔥 <b>Real Users • Accurate • Database Verified</b>
"""

    await message.reply(text)