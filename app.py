from flask import Flask, render_template, request

from api import get_team_matches
from google_calendar import get_calendar_service, register_matches

app = Flask(__name__)


# チーム一覧（ここはUI用）
TEAMS = {
    "Japan": 766,
    "Brazil": 764,
    "France": 773,
    "Germany": 759,
    "Argentina": 762,
}


@app.route("/", methods=["GET", "POST"])
def index():

    message = None
    matches = []

    if request.method == "POST":

        team_id = int(request.form.get("team_id"))

        # ① APIから試合取得
        matches = get_team_matches(team_id)

        # ② Googleカレンダー接続
        service = get_calendar_service()

        # ③ 一括登録
        links = register_matches(service, matches)

        message = f"{len(links)}件カレンダー登録しました"

    return render_template(
        "index.html",
        teams=TEAMS,
        matches=matches,
        message=message
    )


if __name__ == "__main__":
    app.run(debug=True)
