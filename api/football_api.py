import os
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# =========================
# 初期設定
# =========================
load_dotenv()

API_KEY = os.getenv("API_KEY")
JST = timezone(timedelta(hours=9))


# =========================
# JST変換ユーティリティ
# =========================
def to_jst(utc_str):
    return datetime.fromisoformat(
        utc_str.replace("Z", "+00:00")
    ).astimezone(JST)


# =========================
# 過去試合フィルター（重要）
# =========================
def filter_future_matches(matches):
    now = datetime.now(JST)

    return [
        m for m in matches
        if m["start"] >= now
    ]


# =========================
# リーグのチーム取得
# =========================
def get_league_teams(league_code):

    print(f"🌐 get_league_teams: {league_code}")

    url = f"https://api.football-data.org/v4/competitions/{league_code}/teams"

    headers = {
        "X-Auth-Token": API_KEY
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print("❌ request error:", e)
        return {}

    if response.status_code != 200:
        print("❌ API Error:", response.status_code)
        return {}

    data = response.json()

    teams = {}

    for team in data.get("teams", []):
        teams[team["name"]] = team["id"]

    return teams


# =========================
# チームの試合取得（メイン）
# =========================
def get_team_matches(team_id):

    print(f"🌐 get_team_matches: {team_id}")

    url = f"https://api.football-data.org/v4/teams/{team_id}/matches"

    headers = {
        "X-Auth-Token": API_KEY
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print("❌ request error:", e)
        return []

    if response.status_code != 200:
        print("❌ API Error:", response.status_code)
        return []

    data = response.json()

    matches = []

    for match in data.get("matches", []):

        try:
            dt = to_jst(match["utcDate"])

            matches.append({
                "home": match["homeTeam"]["name"],
                "away": match["awayTeam"]["name"],
                "competition": match["competition"]["name"],
                "start": dt,
                "end": dt + timedelta(hours=2),
                "match_id": match["id"]
            })

        except Exception as e:
            print("⚠️ parse error:", e)

    # =========================
    # 🔥重要：未来だけ残す
    # =========================
    matches = filter_future_matches(matches)

    return matches