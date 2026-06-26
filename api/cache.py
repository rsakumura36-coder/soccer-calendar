import json
import os
import time
from typing import Optional, Any

# =========================
# 設定
# =========================
CACHE_DIR = "cache"
CACHE_FILE = os.path.join(CACHE_DIR, "team_cache.json")

TTL_SECONDS = 60 * 60 * 6  # 6時間

# =========================
# 安全初期化
# =========================
def _ensure_cache_dir():
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)


# =========================
# キャッシュ読み込み
# =========================
def load_cache() -> Optional[Any]:

    _ensure_cache_dir()

    if not os.path.exists(CACHE_FILE):
        return None

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 破損チェック
        if "timestamp" not in data or "teams" not in data:
            print("⚠ cache format invalid")
            return None

        # TTLチェック
        if time.time() - data["timestamp"] > TTL_SECONDS:
            print("🕒 cache expired")
            return None

        print("📦 cache使用")
        return data["teams"]

    except json.JSONDecodeError:
        print("❌ cache破損（JSONエラー）")
        return None

    except Exception as e:
        print("❌ cache読み込みエラー:", e)
        return None


# =========================
# キャッシュ保存
# =========================
def save_cache(teams: Any) -> None:

    _ensure_cache_dir()

    try:
        data = {
            "timestamp": time.time(),
            "teams": teams
        }

        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print("💾 cache saved")

    except Exception as e:
        print("❌ cache保存失敗:", e)


# =========================
# キャッシュ削除
# =========================
def clear_cache() -> None:

    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
        print("🗑 cache cleared")
    else:
        print("⚠ cache not found")


# =========================
# キャッシュ強制更新フラグ（拡張用）
# =========================
def is_expired(data: dict) -> bool:

    if not data:
        return True

    return (time.time() - data.get("timestamp", 0)) > TTL_SECONDS