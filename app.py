from flask import Flask, render_template, request, jsonify
from datetime import datetime
import pytz

from api.teams import get_all_teams
from services.match_service import get_processed_matches

app = Flask(__name__)

print("🚀 loading teams...")
ALL_TEAMS = get_all_teams()
print("✅ teams loaded")


# =========================
# JST変換
# =========================
def to_jst(dt):
    if not dt:
        return ""

    jst = pytz.timezone("Asia/Tokyo")
    return dt.astimezone(jst).strftime("%Y-%m-%d %H:%M")


# =========================
# ホーム
# =========================
@app.route("/", methods=["GET", "POST"])
def index():

    selected_league = request.form.get("league", "Premier League")
    teams = ALL_TEAMS.get(selected_league, {})

    matches = []
    message = None

    if request.method == "POST":

        team_id = request.form.get("team_id")
        print("選択された team_id =", team_id)

        if team_id:

            matches = get_processed_matches(int(team_id))

            # JST追加
            for match in matches:
                match["japanDate"] = to_jst(match["start"])

            message = f"{len(matches)}件の試合を取得しました"

    return render_template(
        "index.html",
        leagues=ALL_TEAMS.keys(),
        teams=teams,
        matches=matches,
        message=message,
        selected_league=selected_league,
        all_teams=ALL_TEAMS
    )

@app.route("/api/team/<int:team_id>")
def api_team_matches(team_id):

    matches = get_processed_matches(team_id)

    return jsonify(matches)

if __name__ == "__main__":
    app.run(debug=True)