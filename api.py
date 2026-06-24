import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

load_dotenv()

API_KEY = os.getenv("API_KEY")

JST = timezone(timedelta(hours=9))


def get_team_matches(team_id):
    """
    指定チームIDの試合一覧を取得して返す
    Google Calendar登録用の整形済みデータ
    """

    url = f"https://api.football-data.org/v4/teams/{team_id}/matches"

    headers = {
        "X-Auth-Token": API_KEY
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    # APIエラー対策
    if response.status_code != 200:
        print("API Error:", response.status_code)
        print(data)
        return []

    matches = []

    for match in data.get("matches", []):

        # UTC → JST変換
        dt = datetime.fromisoformat(
            match["utcDate"].replace("Z", "+00:00")
        ).astimezone(JST)

        matches.append({
            "home": match["homeTeam"]["name"],
            "away": match["awayTeam"]["name"],
            "competition": match["competition"]["name"],
            "start": dt,
            "end": dt + timedelta(hours=2),

            # あると後で便利（重複防止・識別用）
            "utc": match["utcDate"],
            "match_id": match["id"]
        })

    return matches


# =========================
# テスト実行用
# =========================
if __name__ == "__main__":

    TEAM_ID = 766  # Japan

    matches = get_team_matches(TEAM_ID)

    for m in matches:
        print("-------------------")
        print(m["start"])
        print(m["home"], "vs", m["away"])
        print(m["competition"])
