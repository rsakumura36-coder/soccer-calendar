import json
import os
import time

os.makedirs("cache", exist_ok=True)

CACHE_FILE = "cache/team_cache.json"
TTL_SECONDS = 60 * 60 * 6  # 6時間


# =========================
# 読み込み
# =========================
def load_cache():

    if not os.path.exists(CACHE_FILE):
        return None

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # TTLチェック
        if time.time() - data["timestamp"] > TTL_SECONDS:
            print("🕒 cache expired")
            return None

        print("📦 TEAM CACHE USED")
        return data["data"]

    except Exception as e:
        print("❌ cache error:", e)
        return None


# =========================
# 保存
# =========================
def save_cache(data):

    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": time.time(),
                "data": data
            }, f, ensure_ascii=False, indent=4)

        print("💾 cache saved")

    except Exception as e:
        print("❌ cache save error:", e)


# =========================
# 手動クリア（便利）
# =========================
def clear_cache():

    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
        print("🗑 cache cleared")