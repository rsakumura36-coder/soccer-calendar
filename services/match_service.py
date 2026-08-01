from api.football_api import get_team_matches, filter_future_matches
from services.match_cache_service import load_match_cache, save_match_cache
from datetime import timezone, timedelta
from datetime import datetime

JST = timezone(timedelta(hours=9))

# =========================
# JST変換（表示用のみ）
# =========================
def to_jst(dt):
    if not dt:
        return None
    return dt.astimezone(JST)

# =========================
# 正規化（軽量）
# =========================
def normalize_match(m):

    return {
        "id": m.get("id"),

        "home": m.get("home"),
        "away": m.get("away"),

        "home_id": m.get("home_id"),
        "away_id": m.get("away_id"),

        "home_logo": m.get("home_logo"),
        "away_logo": m.get("away_logo"),

        "competition": m.get("competition"),

        # UTC本体
        "start_utc": m.get("start_utc"),
    }


# =========================
# メイン処理
# =========================
def get_processed_matches(team_id):

    # キャッシュ確認
    matches = load_match_cache(team_id)

    if matches is not None:

        # JSONから戻した日時をdatetimeへ変換
        for m in matches:
            if isinstance(m.get("start_utc"), str):
                m["start_utc"] = datetime.fromisoformat(
                    m["start_utc"]
                )

    else:

        print("🌐 API FETCH")

        matches = get_team_matches(team_id)
       
        save_match_cache(team_id, matches)

    matches = [normalize_match(m) for m in matches]

    matches = filter_future_matches(matches)

    # JSTはここで付与（表示用）
    for m in matches:
        m["start"] = to_jst(m["start_utc"])
        m["end"] = m["start"] + timedelta(hours=2)

    return matches