from database.db import get_connection
from services.match_service import get_processed_matches
from data.team_names import TEAM_NAMES

from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))

WEEKDAYS = [
    "月",
    "火",
    "水",
    "木",
    "金",
    "土",
    "日"
]


def get_favorites():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            team_id,
            team_name
        FROM favorites
        ORDER BY team_name
    """)

    rows = cursor.fetchall()

    print("DEBUG FAVORITES:", rows, flush=True)

    conn.close()

    return rows

def get_favorite_matches():

    favorites = get_favorites()

    result = []

    for team_id, team_name in favorites:

        matches = get_processed_matches(team_id)

        result.append({
            "team_id": team_id,
            "team_name": team_name,
            "matches": matches
        })

    return result

def create_weekly_report():

    teams = get_favorite_matches()

    # 全チームの試合をまとめる
    all_matches = []

    # 全チームの試合をまとめる
    all_matches = []
    match_ids = set()

    for team in teams:

        for match in team["matches"]:

            if match["id"] not in match_ids:
                all_matches.append(match)
                match_ids.add(match["id"])


    # 日付順
    all_matches.sort(
        key=lambda x: x["start"]
    )


    message = "⚽ Soccer Schedule\n\n"
    message += "【今週の試合予定】\n\n"


    if not all_matches:
        message += "今週の試合はありません"
        return message


    for match in all_matches:

        date = match["start"]

        weekday = WEEKDAYS[date.weekday()]

        date_text = (
            f"{date.month}月{date.day}日"
            f"({weekday}) "
            f"{date.strftime('%H:%M')}"
        )


        message += (
            f"📅 {date_text}\n"
            f"🆚 {match['home_jp']} vs {match['away_jp']}\n"
            f"📍 {match['stadium']}\n\n"
        )


    return message

if __name__ == "__main__":

    favorites = get_favorites()

    print(favorites)