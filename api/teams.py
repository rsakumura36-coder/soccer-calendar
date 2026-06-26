# api/teams.py

from api.cache import load_cache, save_cache


# =========================
# 代表チーム（固定データ）
# =========================
def get_national_teams():
    return {
        "Spain": 760,
        "Argentina": 762,
        "France": 773,
        "England": 770,
        "Brazil": 764,
        "Portugal": 765,
        "Netherlands": 211,
        "Germany": 759,
        "Belgium": 805,
        "Morocco": 793,
        "Japan": 4384,
        "South Korea": 4382,
        "Australia": 4390
    }


# =========================
# 全チーム取得
# =========================
def get_all_teams():

    print(">>> get_all_teams START")

    # -------------------------
    # キャッシュ読み込み
    # -------------------------
    try:
        cached = load_cache()
        if cached:
            print("📦 cache使用")
            return cached
    except Exception as e:
        print("⚠️ cache error:", e)

    print("🌐 API取得中...")

    leagues = {
        "Premier League": "PL",
        "La Liga": "PD",
        "Bundesliga": "BL1",
        "Serie A": "SA",
        "Ligue 1": "FL1"
    }

    all_teams = {}

    # ★ 遅延import（重要）
    try:
        from api.football_api import get_league_teams
    except Exception as e:
        print("❌ football_api import error:", e)
        return {}

    # -------------------------
    # 各リーグ取得
    # -------------------------
    for league_name, league_code in leagues.items():
        try:
            print(f"  → {league_name}")
            all_teams[league_name] = get_league_teams(league_code)
        except Exception as e:
            print(f"⚠️ {league_name} error:", e)
            all_teams[league_name] = {}

    # -------------------------
    # 代表チーム追加
    # -------------------------
    all_teams["National Teams"] = get_national_teams()

    # -------------------------
    # キャッシュ保存
    # -------------------------
    try:
        save_cache(all_teams)
    except Exception as e:
        print("⚠️ save cache error:", e)

    return all_teams