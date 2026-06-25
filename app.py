from flask import Flask, render_template, request

from api import get_team_matches

app = Flask(__name__)

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

        # APIから試合取得
        matches = get_team_matches(team_id)

        message = f"{len(matches)}件の試合を取得しました"

    return render_template(
        "index.html",
        teams=TEAMS,
        matches=matches,
        message=message
    )


if __name__ == "__main__":
    app.run(debug=True)