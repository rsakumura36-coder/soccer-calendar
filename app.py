from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():

    teams = [
        "ガンバ大阪",
        "アーセナル",
        "ブライトン"
    ]

    matches = [
        {
            "date": "6/20 19:00",
            "home": "ガンバ大阪",
            "away": "川崎フロンターレ"
        },
        {
            "date": "6/21 22:00",
            "home": "アーセナル",
            "away": "チェルシー"
        },
        {
            "date": "6/22 20:30",
            "home": "ブライトン",
            "away": "リヴァプール"
        }
    ]

    return render_template(
        "index.html",
        teams=teams,
        matches=matches
    )

if __name__ == "__main__":
    app.run(debug=True)