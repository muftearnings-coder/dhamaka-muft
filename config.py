import os

# =====================
# MongoDB Configuration
# =====================

DATABASE_URI = os.environ.get(
    "DATABASE_URI",
    ""
)

# ⚠️ NOTE:
# Database name = MongoDB me jo database already hai
# Tumhare case me: dreamxbotz (screenshot se confirm)

DATABASE_NAME = os.environ.get(
    "DATABASE_NAME",
    "dreamxbotz"
)

# ⚠️ Collection wahi rakho jo pehle use ho rahi thi
# Tum khud bole the: royal_files

COLLECTION_NAME = os.environ.get(
    "COLLECTION_NAME",
    "royal_files"
)