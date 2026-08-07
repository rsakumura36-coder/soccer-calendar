from flask import Flask, render_template, request, jsonify
from datetime import datetime
import pytz

from api.teams import get_all_teams
from services.match_service import get_processed_matches
from database.db import get_connection

app = Flask(__name__)

ALL_TEAMS = get_all_teams()

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

    print("🔥 API TEAM CALLED:", team_id, flush=True)

    matches = get_processed_matches(team_id)

    print("🔥 MATCH RETURN:", len(matches), flush=True)

    return jsonify(matches)



# =========================
# お気に入り登録
# =========================
@app.route("/api/favorite/add", methods=["POST"])
def add_favorite():

    print("⭐ favorite API called", flush=True)

    data = request.json

    print("DATA:", data, flush=True)

    team_id = data["id"]
    team_name = data["name"]
    logo = data["logo"]


    conn = get_connection()

    cursor = conn.cursor()


    try:

        cursor.execute(
            """
            INSERT OR IGNORE INTO favorites
            (
                team_id,
                team_name,
                logo
            )
            VALUES
            (?, ?, ?)
            """,
            (
                team_id,
                team_name,
                logo
            )
        )

        conn.commit()


    except Exception as e:

        print("favorite save error:", e)


    finally:

        conn.close()


    return jsonify({
        "status": "ok"
    })

# =========================
# お気に入り削除
# =========================
@app.route("/api/favorite/delete", methods=["POST"])
def delete_favorite():

    data = request.json

    team_id = data["id"]


    conn = get_connection()

    cursor = conn.cursor()


    try:

        cursor.execute(
            """
            DELETE FROM favorites
            WHERE team_id = ?
            """,
            (team_id,)
        )

        conn.commit()

        print("🗑 favorite deleted:", team_id, flush=True)


    except Exception as e:

        print("favorite delete error:", e)


    finally:

        conn.close()


    return jsonify({
        "status": "deleted"
    })

# =========================
# LINE Webhook
# =========================
@app.route("/callback", methods=["POST"])
def line_callback():

    data = request.json

    print("📩 LINE EVENT:", data, flush=True)

    return "OK"

if __name__ == "__main__":
    app.run(debug=True)