from api.football_api import get_team_matches, filter_future_matches
from services.match_cache_service import load_match_cache, save_match_cache
from datetime import timezone, timedelta
from datetime import datetime
from data.team_names import TEAM_NAMES
from data.stadiums import STADIUMS

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

    home_id = m.get("home_id")
    away_id = m.get("away_id")

    return {
        "id": m.get("id"),

        # 元データ
        "home": m.get("home"),
        "away": m.get("away"),

        # ID
        "home_id": home_id,
        "away_id": away_id,

        # 日本語名
        "home_jp": TEAM_NAMES.get(
            home_id,
            m.get("home")
        ),

        "away_jp": TEAM_NAMES.get(
            away_id,
            m.get("away")
        ),

        # ロゴ
        "home_logo": m.get("home_logo"),
        "away_logo": m.get("away_logo"),

        # 大会
        "competition": m.get("competition"),

        # スタジアム
        "stadium": STADIUMS.get(
            home_id,
            "スタジアム情報なし"
        ),

        # 元のvenueも残す
        "venue": m.get("venue"),

        # UTC
        "start_utc": m.get("start_utc"),
    }

# =========================
# 金曜〜翌週木曜フィルター
# =========================
def filter_weekly_matches(matches):

    now = datetime.now(JST)

    # 今週金曜日の日付を取得
    days_until_friday = (
        4 - now.weekday()
    ) % 7

    friday = (
        now + timedelta(days=days_until_friday)
    ).replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    # 翌週木曜日の終わりまで
    thursday = friday + timedelta(days=7)

    return [
        m for m in matches
        if friday <= m["start"] < thursday
    ]


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

        if matches:
            save_match_cache(team_id, matches)
        else:
            print("⚠️ API returned empty. Cache not saved.")

    matches = [normalize_match(m) for m in matches]

    print("NORMALIZE COUNT:", len(matches))

    for m in matches[:3]:
        print(
            m["home"],
            m["away"],
            m.get("start_utc")
        )


    matches = filter_future_matches(matches)

    print("FILTER COUNT:", len(matches))


    # JST変換
    for m in matches:
        m["start"] = to_jst(m["start_utc"])
        m["end"] = m["start"] + timedelta(hours=2)


    return matches