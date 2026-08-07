document.addEventListener("DOMContentLoaded", function () {

    const allTeams = window.allTeams || {};

    const leagueSelect = document.querySelector('select[name="league"]');
    const teamSelect = document.querySelector('select[name="team_id"]');

    // =========================
    // DOM安全チェック
    // =========================
    if (!leagueSelect || !teamSelect) {
        console.warn("leagueSelect or teamSelect not found");
        return;
    }

      // =========================
    // チーム更新
    // =========================
    function updateTeams(league) {

        const teams = allTeams?.[league] || {};

        teamSelect.innerHTML = "";

        for (const [name, team] of Object.entries(teams)) {

            const option = document.createElement("option");

            option.value = team.id;

            option.textContent = name;

            option.dataset.logo = team.logo;

            teamSelect.appendChild(option);
        }
    }

    // =========================
    // リーグ変更イベント
    // =========================
    leagueSelect.addEventListener("change", function () {
        updateTeams(this.value);
    });

    // 初期表示
    updateTeams(leagueSelect.value);

    // =========================
    // お気に入り登録（検索画面）
    // =========================
    const favoriteTeamBtn = document.getElementById("favorite-team-btn");

    if (favoriteTeamBtn) {

        favoriteTeamBtn.addEventListener("click", function () {

            const teamId = teamSelect.value;

            const teamName =
                teamSelect.options[teamSelect.selectedIndex].text;

            const logo =
                teamSelect.options[teamSelect.selectedIndex].dataset.logo;


            const team = {
                id: teamId,
                name: teamName,
                logo: logo
            };


            // localStorage取得
            let favorites =
                JSON.parse(localStorage.getItem("favorites")) || [];


            // 重複チェック
            const exists = favorites.some(
                f => f.id === team.id
            );


            if (exists) {

                alert(`${team.name} はすでに登録されています。`);

                return;

            }


            console.log("sending favorite:", team);


            fetch("/api/favorite/add", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(team)

            })
            .then(response => {

                console.log("API response:", response.status);

                return response.json();

            })
            .then(data => {

                console.log("API data:", data);


                // localStorage保存
                favorites.push(team);

                localStorage.setItem(
                    "favorites",
                    JSON.stringify(favorites)
                );


                alert(`${team.name} をお気に入りに登録しました！`);


                renderFavorites();

                loadFavoriteMatches();

            })
            .catch(error => {

                console.error(
                    "favorite save error:",
                    error
                );

            });

        });

    } 

});

// ======================================================
// ⭐ お気に入り機能（登録・削除・表示）
// ======================================================

// =========================
// お気に入り表示
// =========================
function renderFavorites() {

    const list = document.getElementById("favorite-list");

    if (!list) return;


    let favorites =
        JSON.parse(localStorage.getItem("favorites")) || [];


    if (favorites.length === 0) {

        list.innerHTML = `
            <li class="list-group-item text-muted text-center">
                まだお気に入りはありません。
            </li>
        `;

        return;
    }


    const html = favorites.map(team => `

        <li class="list-group-item d-flex justify-content-between align-items-center">


            <button
                class="btn btn-link favorite-team-select d-flex align-items-center"
                data-id="${team.id}">


                ${
                    team.logo
                    ?
                    `<img 
                        src="${team.logo}"
                        width="30"
                        class="me-2"
                    >`
                    :
                    "⚽"
                }


                ${team.name}


            </button>



            <button
                class="btn btn-sm btn-outline-danger remove-favorite"
                data-id="${team.id}">

                ×

            </button>


        </li>


    `).join("");


    list.innerHTML = html;
}

document.addEventListener("click", function (e) {

    // 削除ボタン
    if (e.target.classList.contains("remove-favorite")) {

        const id = e.target.dataset.id;


        fetch("/api/favorite/delete", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                id: id
            })

        })
        .then(response => response.json())

        .then(data => {


            console.log(
                "delete result:",
                data
            );


            let favorites =
                JSON.parse(localStorage.getItem("favorites")) || [];


            favorites = favorites.filter(
                team => team.id !== id
            );


            localStorage.setItem(
                "favorites",
                JSON.stringify(favorites)
            );


            renderFavorites();


        })
        .catch(error => {

            console.error(
                "favorite delete error:",
                error
            );

        });


        return;

    }
    // チーム選択
    if (e.target.classList.contains("favorite-team-select")) {

        const teamId = e.target.dataset.id;

        loadTeamMatches(teamId);

        return;

    }

    //戻る処理
    if (e.target.id === "back-favorites-btn") {

        loadFavoriteMatches();

        e.target.style.display = "none";

        return;

    }


});

// =========================
// お気に入りチームの試合取得
// =========================
function formatDate(dateString) {

    const date = new Date(dateString);

    const month = date.getMonth() + 1;
    const day = date.getDate();

    const week = [
        "日",
        "月",
        "火",
        "水",
        "木",
        "金",
        "土"
    ][date.getDay()];

    const hour = String(
        date.getHours()
    ).padStart(2,"0");

    const minute = String(
        date.getMinutes()
    ).padStart(2,"0");


    return `${month}/${day}(${week}) ${hour}:${minute}`;
}

function translateCompetition(name) {

    const map = {
        "Premier League": "プレミアリーグ",
        "Primera Division": "ラ・リーガ",
        "National Teams": "代表戦"
    };

    return map[name] || name;
}

function renderMatchList(matches) {

    const weekly = document.getElementById("weekly-matches");

    if (!weekly) return;


    weekly.innerHTML = matches.map(item => {

        const match = item.match ?? item;


        return `

        <div class="list-group-item py-3">

            <div class="row align-items-center">

                <!-- 日時 -->
                <div class="col-3 text-muted small">
                    ${formatDate(match.start)}
                </div>


                <!-- 試合 -->
                <div class="col-6 d-flex align-items-center justify-content-center flex-wrap">

                    <!-- Home -->
                    <div class="d-flex align-items-center">

                        <img
                            src="${match.home_logo}"
                            width="28"
                            class="me-2 img-fluid"
                        >

                        <span>
                            ${match.home_jp ?? match.home}
                        </span>

                    </div>


                    <span class="mx-2 fw-bold">
                        vs
                    </span>


                    <!-- Away -->
                    <div class="d-flex align-items-center">

                        <img
                            src="${match.away_logo}"
                            width="30"
                            class="me-2"
                        >

                        <span>
                            ${match.away_jp ?? match.away}
                        </span>

                    </div>

                </div>


                <!-- Stadium -->
                <div class="col-3 text-muted text-end small">

                    <span class="d-none d-md-inline">
                        🏟 ${match.stadium}
                    </span>

                </div>


            </div>

        </div>

        `;

    }).join("");

}

async function loadFavoriteMatches() {

    const favorites =
        JSON.parse(localStorage.getItem("favorites")) || [];

    if (favorites.length === 0) {

        const weekly = document.getElementById("weekly-matches");

        if(weekly){
            weekly.innerHTML =
            "<p class='text-muted text-center'>お気に入りチームを登録してください。</p>";
        }

        return;
    }

    const favoriteMatches = (
        await Promise.all(

            favorites.map(async (team) => {

                const response = await fetch(`/api/team/${team.id}`);

                if (!response.ok) {
                    return null;
                }

                const matches = await response.json();

                const upcomingMatches = matches
                    .filter(match => new Date(match.start) >= new Date())
                    .sort(
                        (a, b) =>
                        new Date(a.start) - new Date(b.start)
                    );

                const nextMatch = upcomingMatches[0];

                if (!nextMatch) {
                    return null;
                }

                return {
                    team,
                    match: nextMatch
                };

            })

        )
    ).filter(item => item !== null);


    // ★追加：試合日時順に並び替え
    favoriteMatches.sort(
        (a, b) =>
        new Date(a.match.start) -
        new Date(b.match.start)
    );

    renderMatchList(favoriteMatches);

    const backBtn = document.getElementById("back-favorites-btn");

    if (backBtn) {
        backBtn.style.display = "none";

    }

}

// =========================
// 選択したチームの直近5試合取得
// =========================

async function loadTeamMatches(teamId) {

    const response = await fetch(`/api/team/${teamId}`);

    if (!response.ok) {
        console.error("API error:", response.status);

        const weekly = document.getElementById("weekly-matches");
        if (weekly) {
            weekly.innerHTML = "<p>試合情報の取得に失敗しました。</p>";
        }
        return;
    }

    const matches = await response.json();

    const backBtn =
    document.getElementById("back-favorites-btn");

    const upcomingMatches = matches.filter(match => {

        return new Date(match.start) >= new Date();

    });


    upcomingMatches.sort((a,b)=>{

        return new Date(a.start)-new Date(b.start);

    });

    const nextMatches = upcomingMatches.slice(0,5);

    if(nextMatches.length === 0){

        const weekly =
            document.getElementById("weekly-matches");

        weekly.innerHTML =
            "<p>今後の試合はありません。</p>";

        return;

    }

    if (backBtn) {

        backBtn.style.display = "block";

    }

    renderMatchList(nextMatches);

}

// =========================
// 初期化
// =========================
renderFavorites();

loadFavoriteMatches();
