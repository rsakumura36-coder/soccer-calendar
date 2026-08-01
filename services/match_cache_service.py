import json
import os
import time

CACHE_FILE = "cache/match_cache.json"
TTL_SECONDS = 60 * 30   # 30分

def load_match_cache(team_id):

    if not os.path.exists(CACHE_FILE):
        return None

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)

    except Exception:
        return None

    # =========================
    # 期限切れキャッシュを一括削除
    # =========================
    changed = False

    for key in list(cache.keys()):

        cache_data = cache[key]

        if time.time() - cache_data["timestamp"] > TTL_SECONDS:

            print(f"🗑 DELETE OLD CACHE: {key}")

            del cache[key]

            changed = True

    if changed:

        with open(CACHE_FILE, "w", encoding="utf-8") as f:

            json.dump(
                cache,
                f,
                ensure_ascii=False,
                indent=2
            )

    team_key = str(team_id)

    if team_key not in cache:
        return None

    cache_data = cache[team_key]

    # ⭐ 有効なキャッシュ
    print("♻️ MATCH CACHE USED")
    return cache_data["matches"]

def save_match_cache(team_id, matches):

    cache = {}

    if os.path.exists(CACHE_FILE):

        try:

            with open(
                CACHE_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                cache = json.load(f)

        except Exception:

            cache = {}

    cache[str(team_id)] = {
        "timestamp": time.time(),
        "matches": matches
    }

    os.makedirs(
        "cache",
        exist_ok=True
    )

    with open(
        CACHE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            cache,
            f,
            ensure_ascii=False,
            indent=2,
            default=str
        )

    print("💾 MATCH CACHE SAVED")