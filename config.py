import os

# ───────── Telegram Config ─────────
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# ───────── Database Config ─────────
DATABASE_URI = os.environ.get("DATABASE_URI", "")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "dreamxbotz")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME", "files")

# ───────── Admin / Channels ─────────
ADMINS = list(map(int, os.environ.get("ADMINS", "").split()))
CHANNELS = list(map(int, os.environ.get("CHANNELS", "").split()))

LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", 0))
BIN_CHANNEL = int(os.environ.get("BIN_CHANNEL", 0))

# ───────── Links ─────────
OWNER_LNK = os.environ.get("OWNER_LNK", "")
GRP_LNK = os.environ.get("GRP_LNK", "")
UPDATE_CHNL_LNK = os.environ.get("UPDATE_CHNL_LNK", "")
FQDN = os.environ.get("FQDN", "")

# ───────── TMDB ─────────
TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")

# ───────── Safety Check ─────────
if not API_ID or not API_HASH or not BOT_TOKEN:
    raise RuntimeError("API_ID / API_HASH / BOT_TOKEN missing")

if not DATABASE_URI:
    raise RuntimeError("DATABASE_URI missing")