import os
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

JST = timezone(timedelta(hours=9))


# =========================
# UTC変換
# =========================
def to_utc(dt_str):
    return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))


# =========================
# チーム取得
# =========================
def get_league_teams(league_code):

    url = f"https://api.football-data.org/v4/competitions/{league_code}/teams"

    headers = {"X-Auth-Token": API_KEY}

    try:
        res = requests.get(url, headers=headers, timeout=10)

    except Exception as e:
        print("❌ request error:", e)
        return {}

    if res.status_code != 200:
        print("❌ API Error:", res.status_code)
        return {}

    data = res.json()


    teams = {}

    for t in data.get("teams", []):

        print(
            t["id"],
            
            t["name"],
            t.get("venue")
        )

        teams[t["name"]] = {

            "id": t["id"],

            "logo": t.get("crest"),

            "venue": t.get("venue")

        }

    return teams

# =========================
# 試合取得（UTC統一）
# =========================
def get_team_matches(team_id):

    print(f"🌐 get_team_matches: {team_id}")

    url = f"https://api.football-data.org/v4/teams/{team_id}/matches"
    headers = {"X-Auth-Token": API_KEY}

    try:
        res = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print("❌ request error:", e)
        return []

    if res.status_code != 200:
        print("❌ API Error:", res.status_code)
        print(res.text)
        return []

    data = res.json()

    # ★追加
    print("API MATCH TOTAL:", len(data.get("matches", [])))

    print(
        "API COMPETITION:",
        data.get("matches", [{}])[0].get("competition")
        if data.get("matches")
        else "NO MATCH"
    )

    matches = []

    for m in data.get("matches", []):

        try:
            start_utc = to_utc(m["utcDate"])

            matches.append({
                "id": m["id"],

                "home": m["homeTeam"]["name"],
                "away": m["awayTeam"]["name"],

                "home_id": m["homeTeam"]["id"],
                "away_id": m["awayTeam"]["id"],

                "home_logo": m["homeTeam"].get("crest"),
                "away_logo": m["awayTeam"].get("crest"),

                "competition": m["competition"]["name"],

                "venue": m.get("venue"),

                # ⭐ 重要：UTCで統一
                "start_utc": start_utc,
                "end_utc": start_utc + timedelta(hours=2),
            })

        except Exception as e:
            print("⚠️ parse error:", e)

    return matches


# =========================
# UTCフィルタ（安全）
# =========================
def filter_future_matches(matches):

    now = datetime.now(timezone.utc)

    return [
        m for m in matches
        if m.get("start_utc") and m["start_utc"] >= now
    ]