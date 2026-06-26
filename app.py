from flask import Flask, render_template, request
import json

from api.teams import get_all_teams
from api.football_api import get_team_matches
from api.cache import clear_cache
from services.calendar_service import add_matches_to_calendar

app = Flask(__name__)

# =========================
# 起動時ロード（キャッシュ or API）
# =========================
print("🚀 loading teams...")
ALL_TEAMS = get_all_teams()
print("✅ teams loaded")


# =========================
# メイン画面
# =========================
@app.route("/", methods=["GET", "POST"])
def index():

    selected_league = request.form.get("league", "Premier League")
    teams = ALL_TEAMS.get(selected_league, {})

    matches = []
    message = None
    calendar_links = []

    # =========================
    # ユーザー操作（試合取得）
    # =========================
    if request.method == "POST":

        team_id = request.form.get("team_id")

        if team_id:

            team_id = int(team_id)

            # 試合取得
            matches = get_team_matches(team_id)

            # カレンダー登録（services）
            calendar_links = add_matches_to_calendar(matches)

            message = f"{len(matches)}件の試合を取得しました"

    return render_template(
        "index.html",
        leagues=ALL_TEAMS.keys(),
        teams=teams,
        matches=matches,
        message=message,
        selected_league=selected_league,
        all_teams=json.dumps(ALL_TEAMS),
        calendar_links=calendar_links
    )


# =========================
# 手動キャッシュ更新
# =========================
@app.route("/refresh")
def refresh_cache():

    # キャッシュ削除
    clear_cache()

    # 再取得（キャッシュ再生成）
    global ALL_TEAMS
    ALL_TEAMS = get_all_teams()

    return "cache refreshed"


# =========================
# 起動
# =========================
if __name__ == "__main__":
    app.run(debug=True)